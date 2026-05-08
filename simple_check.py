# Verificação direta do template sem Flask
import os

print('🔍 VERIFICAÇÃO DIRETA DO TEMPLATE')
print('=' * 50)

template_path = os.path.join('templates', 'pontos_bolsao.html')

if os.path.exists(template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print('Verificando colunas no arquivo pontos_bolsao.html:')
    
    checks = [
        ('Previsão Início</th>', 'Coluna Previsão Início'),
        ('Tempo Projeto (meses)</th>', 'Coluna Tempo Projeto'),
        ('previsao_inicio', 'Campo previsao_inicio'),
        ('tempo_projeto_meses', 'Campo tempo_projeto_meses'),
        ('colspan="10"', 'Colspan para 10 colunas'),
        ('{% for ponto in pontos %}', 'Loop de dados'),
        ('{% else %}', 'Bloco else'),
        ('Nenhum pacote de pontos cadastrado', 'Mensagem vazia')
    ]
    
    for check, description in checks:
        if check in content:
            print(f'  ✅ {description}')
        else:
            print(f'  ❌ {description}')
    
    # Contar colunas
    th_count = content.count('<th>')
    print(f'\n📊 Total de <th> encontrados: {th_count}')
    
    # Procurar pelas linhas específicas
    lines = content.split('\n')
    print('\n🔍 Linhas relevantes:')
    for i, line in enumerate(lines[40:50], 40):  # Linhas 40-50
        if 'th>' in line or 'colspan' in line:
            print(f'  Linha {i+1}: {line.strip()}')
    
else:
    print('❌ Arquivo template não encontrado!')
