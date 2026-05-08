"""
Sistema de Controle de Licenças Fortinet
Suporte a SQLite (local) e PostgreSQL (produção/Render)
"""
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import sqlite3
import os
import shutil
from datetime import datetime
import openpyxl

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'claro-fortinet-2026')
DB_PATH = os.path.join(os.path.dirname(__file__), 'sistema.db')
BACKUP_DIR = os.path.join(os.path.dirname(__file__), 'backups')
ALLOW_DB_RESET = os.environ.get('ALLOW_DB_RESET', '').lower() in ('1', 'true', 'yes', 'on')

# ── Configuração do Banco de Dados ─────────────────────────────────────────────
DATABASE_URL = os.environ.get('DATABASE_URL')
USAR_POSTGRES = DATABASE_URL is not None and 'postgres' in DATABASE_URL

if USAR_POSTGRES:
    import psycopg2
    import psycopg2.extras
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    print(f"🔵 Usando PostgreSQL")
else:
    print(f"🟢 Usando SQLite: {DB_PATH}")

# Credenciais lidas de variáveis de ambiente com fallback local
USUARIO = os.environ.get('USUARIO', 'EstratOpera')
SENHA   = os.environ.get('SENHA', 'Bolsao26')


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logado'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def get_db_connection():
    if USAR_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        conn.autocommit = False
        return conn
    else:
        conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=FULL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA busy_timeout=30000")
        return conn


def execute_query(conn, query, params=None):
    """Executa query compatível com SQLite e PostgreSQL"""
    if USAR_POSTGRES:
        cur = conn.cursor()
        cur.execute(query, params or ())
        return cur
    else:
        if params:
            return conn.execute(query, params)
        return conn.execute(query)


def fetch_all(conn, query, params=None):
    """Retorna todas as linhas compatível SQLite/PostgreSQL"""
    if USAR_POSTGRES:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(query, params or ())
        return cur.fetchall()
    else:
        if params:
            return conn.execute(query, params).fetchall()
        return conn.execute(query).fetchall()


def fetch_one(conn, query, params=None):
    """Retorna uma linha compatível SQLite/PostgreSQL"""
    if USAR_POSTGRES:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(query, params or ())
        return cur.fetchone()
    else:
        if params:
            return conn.execute(query, params).fetchone()
        return conn.execute(query).fetchone()


def dict_from_row(row):
    """Converte row para dict"""
    if row is None:
        return None
    if USAR_POSTGRES:
        return dict(row)
    return dict(row)


def rows_to_dicts(rows):
    """Converte lista de rows para lista de dicts"""
    return [dict_from_row(r) for r in rows]


def init_db():
    """Cria tabelas no banco ativo (SQLite ou PostgreSQL)"""
    if USAR_POSTGRES:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS pontos_bolsao (
                id SERIAL PRIMARY KEY,
                point_pack_number TEXT NOT NULL UNIQUE,
                responsavel TEXT NOT NULL,
                projetos TEXT,
                pontos INTEGER NOT NULL,
                used_amount REAL DEFAULT 0,
                registration_date TEXT,
                expiration_date TEXT,
                previsao_inicio TEXT,
                tempo_projeto_meses INTEGER
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS pontos_utilizados (
                id SERIAL PRIMARY KEY,
                bolsao_id INTEGER REFERENCES pontos_bolsao(id),
                serial_number TEXT NOT NULL,
                dados_cliente TEXT,
                product_model TEXT,
                valor_pontos_dia REAL NOT NULL,
                data_aplicacao TEXT NOT NULL,
                data_fim TEXT
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS base_conciliacao (
                id SERIAL PRIMARY KEY,
                serial_number TEXT NOT NULL,
                description TEXT,
                usage_date TEXT,
                points REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    else:
        conn = sqlite3.connect(DB_PATH, timeout=30)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=FULL")
        conn.execute("PRAGMA foreign_keys=ON")
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS pontos_bolsao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                point_pack_number TEXT NOT NULL UNIQUE,
                responsavel TEXT NOT NULL,
                projetos TEXT,
                pontos INTEGER NOT NULL,
                used_amount REAL DEFAULT 0,
                registration_date TEXT,
                expiration_date TEXT,
                previsao_inicio TEXT,
                tempo_projeto_meses INTEGER
            )
        ''')
        # Adicionar colunas se não existirem (compatibilidade)
        try:
            cur.execute("ALTER TABLE pontos_bolsao ADD COLUMN previsao_inicio TEXT")
        except:
            pass
        try:
            cur.execute("ALTER TABLE pontos_bolsao ADD COLUMN tempo_projeto_meses INTEGER")
        except:
            pass
        cur.execute('''
            CREATE TABLE IF NOT EXISTS pontos_utilizados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bolsao_id INTEGER,
                serial_number TEXT NOT NULL,
                dados_cliente TEXT,
                product_model TEXT,
                valor_pontos_dia REAL NOT NULL,
                data_aplicacao TEXT NOT NULL,
                data_fim TEXT,
                FOREIGN KEY (bolsao_id) REFERENCES pontos_bolsao (id)
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS base_conciliacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial_number TEXT NOT NULL,
                description TEXT,
                usage_date TEXT,
                points REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()


init_db()


def backup_database(label='snapshot'):
    if not os.path.exists(DB_PATH):
        return None
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'sistema_{label}_{timestamp}.db'
    backup_path = os.path.join(BACKUP_DIR, filename)
    shutil.copy2(DB_PATH, backup_path)
    return backup_path


if not USAR_POSTGRES and os.path.exists(DB_PATH):
    backup_database('startup')


# ── Autenticação ──────────────────────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        if request.form['usuario'] == USUARIO and request.form['senha'] == SENHA:
            session['logado'] = True
            return redirect(url_for('dashboard'))
        erro = 'Usuário ou senha incorretos.'
    return render_template('login.html', erro=erro)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ── Dashboard ─────────────────────────────────────────────────────────────────

@app.route('/')
@login_required
def dashboard():
    conn = get_db_connection()
    if USAR_POSTGRES:
        data_fun = "CURRENT_DATE"
        julian = "EXTRACT(EPOCH FROM CURRENT_DATE -"
    else:
        data_fun = "date('now')"
        julian = "julianday('now') - julianday("

    bolsao_summary = fetch_all(conn, '''
        SELECT
            responsavel || ' (' || projetos || ')' as grupo,
            SUM(pontos) as pontos_totais,
            SUM(used_amount) as used_totais_fortinet
        FROM pontos_bolsao
        GROUP BY grupo
    ''')

    utilizados_summary = fetch_all(conn, f'''
        SELECT
            b.responsavel || ' (' || b.projetos || ')' as grupo,
            SUM(pu.valor_pontos_dia * ({julian}pu.data_aplicacao))) as pontos_consumidos_calculado
        FROM pontos_utilizados pu
        JOIN pontos_bolsao b ON pu.bolsao_id = b.id
        GROUP BY grupo
    ''')

    conn.close()

    utilizados_map = {}
    for r in utilizados_summary:
        r = dict_from_row(r)
        utilizados_map[r['grupo']] = r['pontos_consumidos_calculado'] or 0

    dados_dashboard = []
    for item in bolsao_summary:
        item = dict_from_row(item)
        grupo               = item['grupo']
        pontos_totais       = item['pontos_totais'] or 0
        used_fortinet       = item['used_totais_fortinet'] or 0
        pontos_calc         = utilizados_map.get(grupo, 0)
        dados_dashboard.append({
            'grupo':                    grupo,
            'pontos_totais':            pontos_totais,
            'used_totais_fortinet':     used_fortinet,
            'remaining_totais_fortinet': pontos_totais - used_fortinet,
            'pontos_utilizados_analitico': pontos_calc,
            'faltantes_analitico':      pontos_totais - pontos_calc,
            'percent_fortinet':         (used_fortinet / pontos_totais * 100) if pontos_totais else 0,
            'percent_analitico':        (pontos_calc   / pontos_totais * 100) if pontos_totais else 0,
        })

    return render_template('index.html', dashboard_data=dados_dashboard)


# ── Pontos Bolsão ─────────────────────────────────────────────────────────────

@app.route('/pontos_bolsao')
@login_required
def listar_pontos_bolsao():
    conn = get_db_connection()
    pontos = fetch_all(conn, 'SELECT * FROM pontos_bolsao ORDER BY registration_date DESC')
    conn.close()
    return render_template('pontos_bolsao.html', pontos=rows_to_dicts(pontos))


@app.route('/pontos_bolsao/novo', methods=['GET', 'POST'])
@login_required
def novo_ponto_bolsao():
    erro = None
    if request.method == 'POST':
        return _salvar_ponto_bolsao(None)
    return render_template('novo_bolsao.html', ponto=None, erro=erro)


@app.route('/pontos_bolsao/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_ponto_bolsao(id):
    conn = get_db_connection()
    ponto = fetch_one(conn, 'SELECT * FROM pontos_bolsao WHERE id = %s' if USAR_POSTGRES else 'SELECT * FROM pontos_bolsao WHERE id = ?', (id,))
    conn.close()
    
    if ponto is None:
        return redirect(url_for('listar_pontos_bolsao'))
    
    erro = None
    if request.method == 'POST':
        return _salvar_ponto_bolsao(id)
    
    return render_template('novo_bolsao.html', ponto=dict_from_row(ponto), erro=erro)


def _salvar_ponto_bolsao(id_registro):
    erro = None
    try:
        reg_date_str = request.form['registration_date']
        exp_date_str = request.form['expiration_date']
        
        reg_date = datetime.strptime(reg_date_str, '%Y-%m-%d')
        exp_date = datetime.strptime(exp_date_str, '%Y-%m-%d')
        
        if exp_date <= reg_date:
            erro = 'Data de Expiração deve ser posterior à Data de Registro.'
            return render_template('novo_bolsao.html', ponto=None, erro=erro)
        
        if reg_date.year < 2020 or reg_date.year > 2040 or exp_date.year < 2020 or exp_date.year > 2040:
            erro = 'Ano deve estar entre 2020 e 2040. Verifique as datas inseridas.'
            return render_template('novo_bolsao.html', ponto=None, erro=erro)
        
        conn = get_db_connection()
        
        if id_registro is None:
            placeholder = '%s' if USAR_POSTGRES else '?'
            execute_query(conn, f'''
                INSERT INTO pontos_bolsao
                    (point_pack_number, responsavel, projetos, pontos, used_amount, registration_date, expiration_date, previsao_inicio, tempo_projeto_meses)
                VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
            ''', (
                request.form['point_pack_number'],
                request.form['responsavel'],
                request.form['projetos'],
                int(request.form['pontos']),
                float(request.form.get('used_amount') or 0),
                request.form['registration_date'],
                request.form['expiration_date'],
                request.form.get('previsao_inicio') or None,
                int(request.form['tempo_projeto_meses']) if request.form.get('tempo_projeto_meses') else None,
            ))
        else:
            placeholder = '%s' if USAR_POSTGRES else '?'
            execute_query(conn, f'''
                UPDATE pontos_bolsao SET
                    point_pack_number = {placeholder}, responsavel = {placeholder}, projetos = {placeholder},
                    pontos = {placeholder}, used_amount = {placeholder},
                    registration_date = {placeholder}, expiration_date = {placeholder},
                    previsao_inicio = {placeholder}, tempo_projeto_meses = {placeholder}
                WHERE id = {placeholder}
            ''', (
                request.form['point_pack_number'],
                request.form['responsavel'],
                request.form['projetos'],
                int(request.form['pontos']),
                float(request.form.get('used_amount') or 0),
                request.form['registration_date'],
                request.form['expiration_date'],
                request.form.get('previsao_inicio') or None,
                int(request.form['tempo_projeto_meses']) if request.form.get('tempo_projeto_meses') else None,
                id_registro,
            ))
        
        conn.commit()
        conn.close()
        if not USAR_POSTGRES:
            backup_database('pontos_bolsao')
        return redirect(url_for('listar_pontos_bolsao'))
    
    except Exception as e:
        erro = f'Erro ao salvar: {str(e)}'
        if 'UNIQUE' in str(e) or 'duplicate' in str(e):
            erro = 'Número do Pack já cadastrado. Use um número diferente.'
        return render_template('novo_bolsao.html', ponto=None, erro=erro)


# ── Pontos Utilizados ─────────────────────────────────────────────────────────

@app.route('/pontos_utilizados')
@login_required
def listar_pontos_utilizados():
    conn = get_db_connection()
    
    if USAR_POSTGRES:
        query = '''
            SELECT
                pu.id, pu.serial_number, pu.dados_cliente, pu.product_model,
                pu.valor_pontos_dia, pu.data_aplicacao, pu.data_fim,
                b.responsavel || ' (' || b.projetos || ')' as resp_projeto,
                CASE
                    WHEN pu.data_fim IS NULL OR pu.data_fim >= CURRENT_DATE
                    THEN CAST(EXTRACT(EPOCH FROM CURRENT_DATE - pu.data_aplicacao::date)/86400 AS INTEGER)
                    ELSE CAST(EXTRACT(EPOCH FROM pu.data_fim::date - pu.data_aplicacao::date)/86400 AS INTEGER)
                END as dias_consumidos,
                CASE
                    WHEN pu.data_fim IS NULL OR pu.data_fim >= CURRENT_DATE
                    THEN CAST(EXTRACT(EPOCH FROM CURRENT_DATE - pu.data_aplicacao::date)/86400 AS INTEGER)
                    ELSE CAST(EXTRACT(EPOCH FROM pu.data_fim::date - pu.data_aplicacao::date)/86400 AS INTEGER)
                END * pu.valor_pontos_dia as pontos_consumidos
            FROM pontos_utilizados pu
            JOIN pontos_bolsao b ON pu.bolsao_id = b.id
            ORDER BY pu.data_aplicacao DESC
        '''
    else:
        query = '''
            SELECT
                pu.id, pu.serial_number, pu.dados_cliente, pu.product_model,
                pu.valor_pontos_dia, pu.data_aplicacao, pu.data_fim,
                b.responsavel || ' (' || b.projetos || ')' as resp_projeto,
                CASE
                    WHEN pu.data_fim IS NULL OR pu.data_fim >= date('now')
                    THEN CAST(julianday('now') - julianday(pu.data_aplicacao) AS INTEGER)
                    ELSE CAST(julianday(pu.data_fim) - julianday(pu.data_aplicacao) AS INTEGER)
                END as dias_consumidos,
                CASE
                    WHEN pu.data_fim IS NULL OR pu.data_fim >= date('now')
                    THEN CAST(julianday('now') - julianday(pu.data_aplicacao) AS INTEGER)
                    ELSE CAST(julianday(pu.data_fim) - julianday(pu.data_aplicacao) AS INTEGER)
                END * pu.valor_pontos_dia as pontos_consumidos
            FROM pontos_utilizados pu
            JOIN pontos_bolsao b ON pu.bolsao_id = b.id
            ORDER BY pu.data_aplicacao DESC
        '''
    pontos = fetch_all(conn, query)
    conn.close()

    dados = rows_to_dicts(pontos)
    total_pontos = sum(p['pontos_consumidos'] or 0 for p in dados)
    media_pontos = total_pontos / len(dados) if dados else 0
    return render_template('pontos_utilizados.html', data=dados,
                           total_pontos=total_pontos, media_pontos=media_pontos)


@app.route('/pontos_utilizados/novo', methods=['GET', 'POST'])
@login_required
def novo_ponto_utilizado():
    if request.method == 'POST':
        try:
            apl_date_str = request.form['data_aplicacao']
            fim_date_str = request.form.get('data_fim') or None
            
            apl_date = datetime.strptime(apl_date_str, '%Y-%m-%d')
            
            if apl_date.year < 2020 or apl_date.year > 2040:
                flash('Ano da Data Aplicação deve estar entre 2020 e 2040.', 'erro')
                return redirect(url_for('novo_ponto_utilizado'))
            
            if fim_date_str:
                fim_date = datetime.strptime(fim_date_str, '%Y-%m-%d')
                if fim_date.year < 2020 or fim_date.year > 2040:
                    flash('Ano da Data Fim deve estar entre 2020 e 2040.', 'erro')
                    return redirect(url_for('novo_ponto_utilizado'))
                if fim_date <= apl_date:
                    flash('Data Fim deve ser posterior à Data Aplicação!', 'erro')
                    return redirect(url_for('novo_ponto_utilizado'))
            
            conn = get_db_connection()
            placeholder = '%s' if USAR_POSTGRES else '?'
            execute_query(conn, f'''
                INSERT INTO pontos_utilizados
                    (bolsao_id, serial_number, dados_cliente, product_model, valor_pontos_dia, data_aplicacao, data_fim)
                VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
            ''', (
                request.form['bolsao_id'],
                request.form['serial_number'],
                request.form['dados_cliente'],
                request.form['product_model'],
                float(request.form['valor_pontos_dia']),
                request.form['data_aplicacao'],
                request.form.get('data_fim') or None,
            ))
            conn.commit()
            conn.close()
            if not USAR_POSTGRES:
                backup_database('pontos_utilizados')
            return redirect(url_for('listar_pontos_utilizados'))
        except Exception as e:
            flash(f'Erro ao salvar: {str(e)}', 'erro')
            return redirect(url_for('novo_ponto_utilizado'))

    conn = get_db_connection()
    bolsoes = fetch_all(conn, '''
        SELECT id, responsavel, projetos, (pontos - used_amount) as saldo
        FROM pontos_bolsao
        ORDER BY responsavel, projetos, saldo DESC
    ''')
    conn.close()

    grupos_vistos, grupos_unicos = set(), []
    for b in rows_to_dicts(bolsoes):
        chave = (b['responsavel'], b['projetos'])
        if chave not in grupos_vistos:
            grupos_vistos.add(chave)
            grupos_unicos.append(b)

    return render_template('novo_ponto_utilizado.html', bolsoes=grupos_unicos)


# ── Conciliação ───────────────────────────────────────────────────────────────

@app.route('/conciliacao', methods=['GET', 'POST'])
@login_required
def conciliacao():
    conn = get_db_connection()

    if request.method == 'POST':
        arquivo = request.files.get('arquivo_conciliacao')
        if not arquivo or arquivo.filename == '':
            flash('Nenhum arquivo selecionado.', 'erro')
            return redirect(url_for('conciliacao'))

        if os.path.splitext(arquivo.filename)[1].lower() not in ('.xlsx', '.xls'):
            flash('Formato inválido. Envie um arquivo .xlsx ou .xls.', 'erro')
            return redirect(url_for('conciliacao'))

        try:
            wb = openpyxl.load_workbook(arquivo, read_only=True, data_only=True)
            ws = wb.active
            headers = [str(c.value).strip().lower() if c.value else '' for c in next(ws.iter_rows(min_row=1, max_row=1))]

            def col_idx(name):
                for i, h in enumerate(headers):
                    if name.lower() in h:
                        return i
                return None

            idx_serial = col_idx('serial')
            idx_desc   = col_idx('description')
            idx_date   = col_idx('usage date') or col_idx('date')
            idx_points = col_idx('points')

            if idx_serial is None or idx_points is None:
                flash('Colunas obrigatórias não encontradas. O arquivo deve conter "Serial Number" e "Points".', 'erro')
                return redirect(url_for('conciliacao'))

            execute_query(conn, 'DELETE FROM base_conciliacao')
            rows_inseridos = 0
            placeholder = '%s' if USAR_POSTGRES else '?'

            for row in ws.iter_rows(min_row=2, values_only=True):
                serial = row[idx_serial]
                if not serial:
                    continue
                desc   = row[idx_desc]   if idx_desc   is not None else None
                date   = row[idx_date]   if idx_date   is not None else None
                points = row[idx_points] if idx_points is not None else 0

                if isinstance(date, datetime):
                    date = date.strftime('%Y-%m-%d')
                elif date is not None:
                    date = str(date)

                try:
                    points = float(points) if points is not None else 0.0
                except (ValueError, TypeError):
                    points = 0.0

                execute_query(conn,
                    f'INSERT INTO base_conciliacao (serial_number, description, usage_date, points) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})',
                    (str(serial).strip(), str(desc).strip() if desc else '', date, points)
                )
                rows_inseridos += 1

            conn.commit()
            flash(f'Base importada com sucesso! {rows_inseridos} registros carregados.', 'sucesso')
            if not USAR_POSTGRES:
                backup_database('conciliacao')

        except Exception as e:
            flash(f'Erro ao processar o arquivo: {str(e)}', 'erro')
        finally:
            conn.close()

        return redirect(url_for('conciliacao'))

    if USAR_POSTGRES:
        query = '''
            SELECT
                pu.serial_number, pu.dados_cliente, pu.product_model,
                b.responsavel || ' (' || b.projetos || ')' AS grupo,
                pu.valor_pontos_dia, pu.data_aplicacao,
                CASE
                    WHEN pu.data_fim IS NULL OR pu.data_fim >= CURRENT_DATE
                    THEN CAST(EXTRACT(EPOCH FROM CURRENT_DATE - pu.data_aplicacao::date)/86400 AS INTEGER)
                    ELSE CAST(EXTRACT(EPOCH FROM pu.data_fim::date - pu.data_aplicacao::date)/86400 AS INTEGER)
                END AS dias_consumidos,
                CASE
                    WHEN pu.data_fim IS NULL OR pu.data_fim >= CURRENT_DATE
                    THEN CAST(EXTRACT(EPOCH FROM CURRENT_DATE - pu.data_aplicacao::date)/86400 AS INTEGER)
                    ELSE CAST(EXTRACT(EPOCH FROM pu.data_fim::date - pu.data_aplicacao::date)/86400 AS INTEGER)
                END * pu.valor_pontos_dia AS pontos_calculados,
                COALESCE((
                    SELECT SUM(bc.points) FROM base_conciliacao bc
                    WHERE UPPER(TRIM(bc.serial_number)) = UPPER(TRIM(pu.serial_number))
                ), 0) AS pontos_fortinet
            FROM pontos_utilizados pu
            JOIN pontos_bolsao b ON pu.bolsao_id = b.id
            ORDER BY grupo, pu.serial_number
        '''
    else:
        query = '''
            SELECT
                pu.serial_number, pu.dados_cliente, pu.product_model,
                b.responsavel || ' (' || b.projetos || ')' AS grupo,
                pu.valor_pontos_dia, pu.data_aplicacao,
                CASE
                    WHEN pu.data_fim IS NULL OR pu.data_fim >= date('now')
                    THEN CAST(julianday('now') - julianday(pu.data_aplicacao) AS INTEGER)
                    ELSE CAST(julianday(pu.data_fim) - julianday(pu.data_aplicacao) AS INTEGER)
                END AS dias_consumidos,
                CASE
                    WHEN pu.data_fim IS NULL OR pu.data_fim >= date('now')
                    THEN CAST(julianday('now') - julianday(pu.data_aplicacao) AS INTEGER)
                    ELSE CAST(julianday(pu.data_fim) - julianday(pu.data_aplicacao) AS INTEGER)
                END * pu.valor_pontos_dia AS pontos_calculados,
                COALESCE((
                    SELECT SUM(bc.points) FROM base_conciliacao bc
                    WHERE UPPER(TRIM(bc.serial_number)) = UPPER(TRIM(pu.serial_number))
                ), 0) AS pontos_fortinet
            FROM pontos_utilizados pu
            JOIN pontos_bolsao b ON pu.bolsao_id = b.id
            ORDER BY grupo, pu.serial_number
        '''
    resultado = fetch_all(conn, query)

    total_base = fetch_one(conn, 'SELECT COUNT(*) as c FROM base_conciliacao')
    total_base = dict_from_row(total_base)['c'] if total_base else 0
    conn.close()

    linhas = []
    for r in rows_to_dicts(resultado):
        calc     = r['pontos_calculados'] or 0
        fortinet = r['pontos_fortinet']   or 0
        diff     = calc - fortinet
        status   = 'ok' if abs(diff) < 0.01 else ('acima' if diff > 0 else 'abaixo')
        linhas.append({**r, 'diferenca': diff, 'status': status})

    return render_template('conciliacao.html', linhas=linhas, total_base=total_base)


# ── Admin ─────────────────────────────────────────────────────────────────────

@app.route('/admin/limpar-banco', methods=['POST'])
@login_required
def limpar_banco():
    if not ALLOW_DB_RESET:
        flash('Limpeza do banco desabilitada neste ambiente.', 'erro')
        return redirect(url_for('dashboard'))

    if not USAR_POSTGRES:
        backup_database('before_reset')
    
    conn = get_db_connection()
    execute_query(conn, 'DELETE FROM pontos_utilizados')
    execute_query(conn, 'DELETE FROM base_conciliacao')
    execute_query(conn, 'DELETE FROM pontos_bolsao')
    
    if not USAR_POSTGRES:
        try:
            execute_query(conn, 'DELETE FROM sqlite_sequence')
        except:
            pass
    
    conn.commit()
    conn.close()
    flash('Banco de dados limpo com sucesso!', 'sucesso')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')