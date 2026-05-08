# Sistema de Controle de Licenças Fortinet

Sistema web para gerenciamento, controle de consumo e conciliação de licenças Fortinet baseadas em pontos. Desenvolvido em Python/Flask com banco de dados SQLite.

**URL em produção:** https://bolsao.onrender.com

---

## Funcionalidades

- **Login seguro** — acesso protegido por usuário e senha com tela de autenticação
- **Dashboard** — visão consolidada por grupo (Responsável + Projeto) com pontos totais, consumidos, saldo e percentual de utilização
- **Pontos Bolsão** — cadastro e listagem dos Point Packs adquiridos
- **Pontos Utilizados** — registro de equipamentos FortiGate com cálculo automático de consumo diário
- **Conciliação** — upload da base oficial da Fortinet (.xlsx) e cruzamento automático por Serial Number

---

## Acesso ao sistema

| Campo | Valor |
|---|---|
| URL | https://bolsao.onrender.com |
| Usuário | EstratOpera |
| Senha | Bolsao26 |

> ⚠️ Qualquer página acessada sem login redireciona automaticamente para a tela de autenticação.

---

## Tecnologias

- Python 3.14
- Flask 3.0.3
- SQLite (via módulo nativo `sqlite3`) com WAL mode para concorrência
- openpyxl 3.1.2 (leitura de arquivos Excel)
- Gunicorn 22.0.0 (produção)

---

## Instalação e execução local

### 1. Clone o repositório

```bash
git clone https://github.com/carloscostato-cmyk/Bolsao.git
cd Bolsao
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Rode o servidor

```bash
python app.py
```

Acesse em: **http://127.0.0.1:5000**

> O banco de dados (`sistema.db`) e as tabelas são criados automaticamente na primeira execução.

---

## Estrutura do projeto

```
sistema_py/
├── app.py                      # Rotas, lógica principal e autenticação (Flask)
├── wsgi.py                     # Entry point para produção (Gunicorn)
├── Procfile                    # Configuração de deploy (gunicorn app:app)
├── requirements.txt            # Dependências Python
├── sistema.db                  # Banco de dados SQLite
├── static/
│   ├── claro.css               # Estilos globais
│   └── claro_empresasII.jpg    # Logo Claro Empresas
└── templates/
    ├── login.html              # Tela de login
    ├── index.html              # Dashboard
    ├── pontos_bolsao.html      # Listagem de Point Packs
    ├── novo_bolsao.html        # Formulário de novo bolsão
    ├── pontos_utilizados.html  # Listagem de equipamentos
    ├── novo_ponto_utilizado.html # Formulário de novo consumo
    └── conciliacao.html        # Upload e resultado da conciliação
```

---

## Banco de dados

O banco é inicializado automaticamente pelo `app.py` ao subir. Usa **WAL mode** para evitar travamentos em ambiente de produção.

### `pontos_bolsao`
Armazena os pacotes de pontos adquiridos (Point Packs).

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| point_pack_number | TEXT UNIQUE | Identificador único do pacote (ex: ELAVM...) |
| responsavel | TEXT | Equipe: Delivery, Projetos Especiais, Produtos |
| projetos | TEXT | Subprojeto: Pull, SIEM, Aeronáltica, etc. |
| pontos | INTEGER | Total de pontos do pacote |
| used_amount | REAL | Pontos já utilizados (base Fortinet) |
| registration_date | TEXT | Data de registro (AAAA-MM-DD) |
| expiration_date | TEXT | Data de expiração (AAAA-MM-DD) |

### `pontos_utilizados`
Registra cada equipamento FortiGate e seu consumo diário.

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| bolsao_id | INTEGER | FK para `pontos_bolsao` |
| serial_number | TEXT | Serial do equipamento |
| dados_cliente | TEXT | Nome do cliente/site |
| product_model | TEXT | Modelo (FG120G, FG2H0G, etc.) |
| valor_pontos_dia | REAL | Custo em pontos por dia |
| data_aplicacao | TEXT | Data de início do consumo |
| data_fim | TEXT | Data de término (opcional — vazio = ativo) |

### `base_conciliacao`
Base oficial exportada da Fortinet. Substituída integralmente a cada upload.

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| serial_number | TEXT | Serial do equipamento |
| description | TEXT | Descrição |
| usage_date | TEXT | Data do consumo registrado |
| points | REAL | Pontos consumidos na data |

---

## Lógica de cálculo

```
Dias Consumidos   = hoje − data_aplicacao  (ou data_fim − data_aplicacao se encerrado)
Pontos Calculados = valor_pontos_dia × dias_consumidos

Conciliação = SUM(points) da base_conciliacao WHERE serial_number = serial do equipamento
Diferença   = Pontos Calculados − Pontos Fortinet
```

---

## Segurança

- Todas as rotas protegidas com `@login_required` — sem login não acessa nada
- Senhas armazenadas com hash `bcrypt` (sem senha em texto puro no banco)
- Proteção CSRF em todos os formulários `POST`
- Rate limit no login: bloqueio temporário após 5 tentativas inválidas
- Perfis de acesso por usuário (`admin`, `viewer`), com rotas administrativas restritas
- Queries com parâmetros `?` — proteção contra SQL injection
- `secret_key` configurada para proteção de sessão Flask
- WAL mode no SQLite — evita `database is locked` em produção
- `foreign_keys=ON` e `synchronous=FULL` no SQLite — melhora a integridade e a durabilidade das gravações
- Backups automáticos do arquivo `sistema.db` são gerados em `backups/` após cadastros e importações
- Um backup de inicialização é gerado quando a aplicação sobe e encontra `sistema.db`
- A rota administrativa de limpeza do banco fica desativada por padrão e só pode ser habilitada com `ALLOW_DB_RESET=1`

### Logs (opção B escolhida)
- Aplicar mascaramento de dados sensíveis nos logs (não registrar senha/token).
- Manter logs de autenticação (sucesso/falha/bloqueio), ações administrativas e exportações.
- Definir retenção mínima e rotação de arquivos para não crescer indefinidamente.
- Validar acesso aos logs apenas para perfil `admin`.

### Repositório privado no GitHub
1. Abrir o repositório no GitHub.
2. `Settings` > `General` > `Danger Zone`.
3. Selecionar `Change repository visibility`.
4. Escolher `Make private` e confirmar.

> Essa ação é feita no GitHub (configuração da plataforma), não no código da aplicação.

> Observação importante: backup local ajuda contra erro humano e falhas simples, mas não substitui um banco persistente fora do disco da aplicação. Em ambiente hospedado, o ideal é usar um disco persistente ou migrar para um banco gerenciado.

---

## Deploy (produção — Render.com)

O projeto usa `Procfile` com:

```
web: gunicorn app:app
```

O Render detecta automaticamente novos commits no branch `master` e faz redeploy.

---

## Responsáveis

| Área | Responsável |
|---|---|
| Delivery | Equipe Delivery |
| Projetos Especiais | Equipe Projetos Especiais |
| Produtos | Equipe Produtos |
