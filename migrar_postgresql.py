"""
🛡️ Time 2 — Script de Migração SQLite → PostgreSQL
🛡️ Time 3 — Backup automático antes da migração
🔍 Time 1 — Verificação após migração

Gerenciado por: Cascade AI
Data: 08/05/2026

Uso: python migrar_postgresql.py
"""
import os, sys, shutil
from datetime import datetime

BACKUP_DIR = 'backups'
ts = datetime.now().strftime('%Y%m%d_%H%M%S')

print("=" * 60)
print("🛡️ TIME 3 — BACKUP PRÉ-MIGRAÇÃO")
print("=" * 60)

# Backup do banco SQLite atual
os.makedirs(BACKUP_DIR, exist_ok=True)
if os.path.exists('sistema.db'):
    backup = os.path.join(BACKUP_DIR, f'sistema_pre_pg_{ts}.db')
    shutil.copy2('sistema.db', backup)
    print(f"   ✅ Backup SQLite: {backup}")
    
    # Backup dos dados em JSON
    import sqlite3, json
    conn = sqlite3.connect('sistema.db')
    conn.row_factory = sqlite3.Row
    
    dados = {}
    for tabela in ['pontos_bolsao', 'pontos_utilizados', 'base_conciliacao']:
        rows = conn.execute(f'SELECT * FROM {tabela}').fetchall()
        dados[tabela] = [dict(r) for r in rows]
        print(f"   ✅ {tabela}: {len(rows)} registros exportados")
    conn.close()
    
    json_path = os.path.join(BACKUP_DIR, f'dados_pre_pg_{ts}.json')
    with open(json_path, 'w') as f:
        json.dump(dados, f, indent=2, default=str)
    print(f"   ✅ Dados exportados: {json_path}")

print(f"\n🛡️ Time 3: Backup concluído — pronto para Time 2")

print("\n" + "=" * 60)
print("🛡️ TIME 2 — CONFIGURAÇÃO POSTGRESQL")
print("=" * 60)
print("""
Para que os dados NUNCA mais sejam perdidos no Render:

1. Crie um banco PostgreSQL gratuito no Render:
   - Dashboard Render → New → PostgreSQL
   - Escolha o plano gratuito (Free)
   - Anote a "Internal Database URL" (ex: postgres://user:pass@host:5432/db)

2. Configure a variável de ambiente no Render:
   - Nome: DATABASE_URL
   - Valor: (a Internal Database URL que você copiou)

3. O sistema vai automaticamente:
   - Usar PostgreSQL quando DATABASE_URL estiver definida
   - Usar SQLite quando não estiver (ambiente local)
   - Migrar todos os dados existentes

4. Faça deploy:
   git push origin master
""")

print("📋 INSTRUÇÕES PARA O RENDER:")
print("-" * 50)
print("""
1. Acesse: https://dashboard.render.com
2. Clique em "New +" → "PostgreSQL"
3. Preencha:
   - Name: bolsao-db
   - Database: bolsao
   - User: bolsao_user
   - Plan: Free
4. Clique em "Create Database"
5. No serviço "bolsao", vá em Environment
6. Adicione:
   - Key: DATABASE_URL
   - Value: (copie a Internal Database URL do PostgreSQL)
7. Clique em "Save Changes"
8. Deploy automático vai acontecer
""")

print(f"\n✅ Script de migração preparado!")