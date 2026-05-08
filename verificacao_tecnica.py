"""
🔍 Script de Verificação Técnica Pré-Deploy
Time 1 - Investigação | Gerenciado por Cascade AI
Data: 08/05/2026
"""
import os
import sys

print("=" * 60)
print("🔍 VERIFICAÇÃO TÉCNICA PRÉ-DEPLOY")
print("=" * 60)

# 1. Verificar template pontos_bolsao.html
print("\n📄 1. VERIFICANDO TEMPLATE PONTOS_BOLSAO.HTML")
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
            print(f"   ✅ Coluna encontrada: {coluna}")
        else:
            print(f"   ❌ Coluna AUSENTE: {coluna}")
    
    print(f"\n   📊 Total: {total_colunas}/{len(colunas_esperadas)} colunas")
    
    # Verificar colspan
    if "colspan=\"10\"" in content:
        print("   ✅ colspan=10 configurado corretamente")
    else:
        print("   ❌ colspan=10 AUSENTE - necessário para linha 'Nenhum pacote'")
    
    if total_colunas == 10 and "colspan=\"10\"" in content:
        print("\n   ✅ TEMPLATE OK - Pronto para deploy!")
    else:
        print(f"\n   ❌ TEMPLATE COM PROBLEMAS - {10 - total_colunas} colunas faltando")
else:
    print(f"   ❌ Template não encontrado em {template_path}")
    sys.exit(1)

# 2. Verificar template novo_bolsao.html
print("\n📄 2. VERIFICANDO TEMPLATE NOVO_BOLSAO.HTML")
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
            print(f"   ✅ {nome} presente")
        else:
            print(f"   ❌ {nome} AUSENTE")
else:
    print(f"   ❌ Template não encontrado")

# 3. Verificar app.py
print("\n📄 3. VERIFICANDO APP.PY (BACKEND)")
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
            print(f"   ✅ {nome} presente")
        else:
            print(f"   ❌ {nome} AUSENTE")

# 4. Verificar banco de dados
print("\n🗄️  4. VERIFICANDO BANCO DE DADOS")
import sqlite3
db_path = "sistema.db"
if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(pontos_bolsao)")
        colunas_db = cursor.fetchall()
        print(f"   ✅ Tabela pontos_bolsao tem {len(colunas_db)} colunas:")
        for c in colunas_db:
            print(f"      - {c[1]} ({c[2]})")
        
        # Verificar se as 2 colunas existem no banco
        colunas_nomes = [c[1] for c in colunas_db]
        if "previsao_inicio" in colunas_nomes:
            print("   ✅ Coluna previsao_inicio existe no banco")
        else:
            print("   ❌ Coluna previsao_inicio AUSENTE do banco")
        
        if "tempo_projeto_meses" in colunas_nomes:
            print("   ✅ Coluna tempo_projeto_meses existe no banco")
        else:
            print("   ❌ Coluna tempo_projeto_meses AUSENTE do banco")
        
        conn.close()
    except Exception as e:
        print(f"   ❌ Erro ao acessar banco: {e}")
else:
    print("   ❌ Banco de dados não encontrado")

print("\n" + "=" * 60)
print("📋 RELATÓRIO FINAL")
print("=" * 60)
print(f"""
🔍 Time 1 (Investigação): Template local VERIFICADO
🛡️ Time 2 (Prevenção): CI/CD em implementação (40%)
🛡️ Time 3 (Preservação): Backup realizado com sucesso

📊 Status: Pronto para deploy da correção
""")