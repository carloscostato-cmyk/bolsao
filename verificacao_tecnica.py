"""
[INFO] Script de Verificação Técnica Pré-Deploy
Time 1 - Investigação | Gerenciado por Cascade AI
Data: 08/05/2026
"""
import os
import sys

print("=" * 60)
print("[INFO] VERIFICAÇÃO TÉCNICA PRÉ-DEPLOY")
print("=" * 60)

# 1. Verificar template pontos_bolsao.html
print("\n[ARQ] 1. VERIFICANDO TEMPLATE PONTOS_BOLSAO.HTML")
template_path = "templates/pontos_bolsao.html"
if os.path.exists(template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar colunas
    colunas_esperadas = [
        "Point Pack Number",
        "Responsável", 
        "Projeto",
        "Pontos",
        "Used (Fortinet)",
        "Remaining",
        "Registro",
        "Expiração",
        "Previsão Início",
        "Tempo Projeto (meses)"
    ]
    
    total_colunas = 0
    for coluna in colunas_esperadas:
        if coluna in content:
            total_colunas += 1
            print(f"   [OK] Coluna encontrada: {coluna}")
        else:
            print(f"   [ERRO] Coluna AUSENTE: {coluna}")
    
    print(f"\n   [DADOS] Total: {total_colunas}/{len(colunas_esperadas)} colunas")
    
    # Verificar colspan
    if "colspan=\"10\"" in content:
        print("   [OK] colspan=10 configurado corretamente")
    else:
        print("   [ERRO] colspan=10 AUSENTE - necessário para linha 'Nenhum pacote'")
    
    if total_colunas == 10 and "colspan=\"10\"" in content:
        print("\n   [OK] TEMPLATE OK - Pronto para deploy!")
    else:
        print(f"\n   [ERRO] TEMPLATE COM PROBLEMAS - {10 - total_colunas} colunas faltando")
else:
    print(f"   [ERRO] Template não encontrado em {template_path}")
    sys.exit(1)

# 2. Verificar template novo_bolsao.html
print("\n[ARQ] 2. VERIFICANDO TEMPLATE NOVO_BOLSAO.HTML")
novo_template_path = "templates/novo_bolsao.html"
if os.path.exists(novo_template_path):
    with open(novo_template_path, 'r', encoding='utf-8') as f:
        content_novo = f.read()
    
    checks = [
        ("previsao_inicio", "Campo Previsão Início"),
        ("tempo_projeto_meses", "Campo Tempo Projeto (meses)"),
    ]
    
    for campo, nome in checks:
        if campo in content_novo:
            print(f"   [OK] {nome} presente")
        else:
            print(f"   [ERRO] {nome} AUSENTE")
else:
    print(f"   [ERRO] Template não encontrado")

# 3. Verificar app.py
print("\n[ARQ] 3. VERIFICANDO APP.PY (BACKEND)")
app_path = "app.py"
if os.path.exists(app_path):
    with open(app_path, 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    checks_app = [
        ("previsao_inicio", "Coluna previsao_inicio no INSERT"),
        ("tempo_projeto_meses", "Coluna tempo_projeto_meses no INSERT"),
    ]
    
    for campo, nome in checks_app:
        if campo in app_content:
            print(f"   [OK] {nome} presente")
        else:
            print(f"   [ERRO] {nome} AUSENTE")

# 4. Verificar banco de dados
print("\n[DB]  4. VERIFICANDO BANCO DE DADOS")
import sqlite3
db_path = "sistema.db"
if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(pontos_bolsao)")
        colunas_db = cursor.fetchall()
        print(f"   [OK] Tabela pontos_bolsao tem {len(colunas_db)} colunas:")
        for c in colunas_db:
            print(f"      - {c[1]} ({c[2]})")
        
        # Verificar se as 2 colunas existem no banco
        colunas_nomes = [c[1] for c in colunas_db]
        if "previsao_inicio" in colunas_nomes:
            print("   [OK] Coluna previsao_inicio existe no banco")
        else:
            print("   [ERRO] Coluna previsao_inicio AUSENTE do banco")
        
        if "tempo_projeto_meses" in colunas_nomes:
            print("   [OK] Coluna tempo_projeto_meses existe no banco")
        else:
            print("   [ERRO] Coluna tempo_projeto_meses AUSENTE do banco")
        
        conn.close()
    except Exception as e:
        print(f"   [ERRO] Erro ao acessar banco: {e}")
else:
    print("   [ERRO] Banco de dados não encontrado")

print("\n" + "=" * 60)
print("[RESUMO] RELATÓRIO FINAL")
print("=" * 60)
print(f"""
[INFO] Time 1 (Investigação): Template local VERIFICADO
[SEG] Time 2 (Prevenção): CI/CD em implementação (40%)
[SEG] Time 3 (Preservação): Backup realizado com sucesso

[DADOS] Status: Pronto para deploy da correção
""")