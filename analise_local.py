import requests
import sqlite3
import os

# Testar todas as rotas principais
rotas = [
    ('/', 'Dashboard'),
    ('/login', 'Login'),
    ('/pontos_bolsao', 'Pontos Bolsão'),
    ('/pontos_utilizados', 'Pontos Utilizados'),
    ('/conciliacao', 'Conciliação')
]

print('🔍 ANÁLISE DAS ROTAS LOCAIS')
print('=' * 50)

s = requests.Session()
for rota, nome in rotas:
    try:
        r = s.get(f'http://localhost:5000{rota}')
        status = '✅ OK' if r.status_code == 200 else '❌ ERRO'
        print(f'{nome:20} | {rota:20} | {status} ({r.status_code})')
    except Exception as e:
        print(f'{nome:20} | {rota:20} | ❌ ERRO: {str(e)[:30]}')

# Verificar banco de dados
print('\n📊 ANÁLISE DO BANCO DE DADOS')
print('=' * 50)

if os.path.exists('sistema.db'):
    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    
    tabelas = ['pontos_bolsao', 'pontos_utilizados', 'base_conciliacao']
    for tabela in tabelas:
        try:
            cursor.execute(f'SELECT COUNT(*) FROM {tabela}')
            count = cursor.fetchone()[0]
            print(f'{tabela:20} | {count:10} registros')
        except:
            print(f'{tabela:20} | {"Não existe":10}')
    
    conn.close()
else:
    print('❌ Banco de dados não encontrado')
