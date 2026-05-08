import requests
import re

print('🔍 DEBUG FINAL - VERIFICAÇÃO COMPLETA')
print('=' * 50)

try:
    # Acessar a página real
    response = requests.get('http://localhost:5000/pontos_bolsao')
    
    if response.status_code == 200:
        html = response.text
        
        print('📋 ANÁLISE DO HTML RECEBIDO:')
        
        # Procurar por todas as tags <th>
        th_pattern = r'<th[^>]*>(.*?)</th>'
        th_matches = re.findall(th_pattern, html, re.IGNORECASE)
        
        print(f'\nColunas encontradas ({len(th_matches)} total):')
        for i, col in enumerate(th_matches, 1):
            print(f'  {i:2d}. {col.strip()}')
        
        # Verificar colunas específicas
        colunas_chave = ['Previsão Início', 'Tempo Projeto', 'Expiração']
        
        print('\n🔍 Verificação de colunas chave:')
        for coluna in colunas_chave:
            encontrada = any(coluna in col for col in th_matches)
            status = '✅' if encontrada else '❌'
            print(f'  {status} {coluna}')
        
        # Verificar colspan
        colspan_pattern = r'colspan="(\d+)"'
        colspan_matches = re.findall(colspan_pattern, html)
        
        print(f'\n📊 Colspan encontrados: {colspan_matches}')
        
        # Verificar mensagem de tabela vazia
        if 'Nenhum pacote de pontos cadastrado' in html:
            print('✅ Mensagem de tabela vazia presente')
        else:
            print('❌ Mensagem de tabela vazia ausente')
        
        # Salvar HTML para inspeção manual
        with open('debug_output.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print('\n📄 HTML completo salvo em: debug_output.html')
        
        # Análise final
        if len(th_matches) >= 10:
            print('\n✅ SUCESSO: Template com 10+ colunas detectado!')
        else:
            print(f'\n❌ PROBLEMA: Apenas {len(th_matches)} colunas encontradas')
            print('   Esperado: 10 colunas')
            print('   Possível causa: Template antigo em cache')
        
    else:
        print(f'❌ Erro HTTP: {response.status_code}')
        
except Exception as e:
    print(f'❌ Erro na verificação: {e}')

print(f'\n⏰ Verificação finalizada em: {datetime.now().strftime("%H:%M:%S")}')
