"""
🛡️ Time 3 (Preservação) — Backup antes das alterações
Gerenciado por: Cascade AI
Data: 08/05/2026
"""
import os, shutil
from datetime import datetime

BACKUP_DIR = 'backups'
os.makedirs(BACKUP_DIR, exist_ok=True)
ts = datetime.now().strftime('%Y%m%d_%H%M%S')

print("=" * 60)
print("🛡️ TIME 3 — BACKUP DE SEGURANÇA PRÉ-ALTERAÇÃO")
print("=" * 60)

backups = [
    ('sistema.db', f'sistema_antes_edicao_{ts}.db'),
    ('templates/pontos_bolsao.html', f'pontos_bolsao_antes_edicao_{ts}.html'),
    ('templates/novo_bolsao.html', f'novo_bolsao_antes_edicao_{ts}.html'),
    ('app.py', f'app_antes_edicao_{ts}.py'),
]

for origem, destino in backups:
    if os.path.exists(origem):
        shutil.copy2(origem, os.path.join(BACKUP_DIR, destino))
        print(f"   ✅ {origem} → backups/{destino}")
    else:
        print(f"   ⚠️ {origem} não encontrado")

print(f"\n📋 Time 3: {len(backups)} backups criados com sucesso!")
print(f"📋 Pronto para Time 2 implementar a edição.")