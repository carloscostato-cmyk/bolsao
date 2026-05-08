import requests
import re

print('🔍 TESTE COM AUTENTICAÇÃO')
print('=' * 50)

# Criar sessão e fazer login
session = requests.Session()

# Fazer login primeiro
login_data = {
    'usuario': 'EstratOpera',
    'senha': 'Bolsao26'
}

try:
    print('🔐 Fazendo login...')
    login_response = session.post('http://localhost:5000/login', data=login_data)
    
    if login_response.status_code == 302:  # Redirect após login
        print('✅ Login realizado com sucesso!')
        
        # Agora acessar a página de pontos bolsão
        print('📋 Acessando página de Pontos Bolsão...')
        response = session.get('http://localhost:5000/pontos_bolsao')
        
        if response.status_code == 200:
            html = response.text
            
            # Verificar se estamos na página correta
            if 'Pontos Bolsão' in html and 'Catálogo de Pacotes de Pontos' in html:
                print('✅ Página correta carregada!')
                
                # Procurar por todas as tags <th>
                th_pattern = r'<th[^>]*>(.*?)</th>'
                th_matches = re.findall(th_pattern, html, re.IGNORECASE)
                
                print(f'\n📊 Colunas encontradas ({len(th_matches)} total):')
                for i, col in enumerate(th_matches, 1):
                    print(f'  {i:2d}. {col.strip()}')
                
                # Verificar colunas específicas
                colunas_chave = ['Previsão Início', 'Tempo Projeto', 'Expiração', 'Registro']
                
                print('\n🔍 Verificação de colunas chave:')
                for coluna in colunas_chave:
                    encontrada = any(coluna in col for col in th_matches)
                    status = '✅' if encontrada else '❌'
                    print(f'  {status} {coluna}')
                
                # Verificar colspan
                colspan_pattern = r'colspan="(\d+)"'
                colspan_matches = re.findall(colspan_pattern, html)
                print(f'\n📊 Colspan encontrados: {colspan_matches}')
                
                # Análise final
                if len(th_matches) >= 10:
                    print('\n✅ SUCESSO: Template com 10+ colunas!')
                    print('✅ Ambiente local está CORRETO e ATUALIZADO')
                else:
                    print(f'\n❌ PROBLEMA: Apenas {len(th_matches)} colunas')
                    print('❌ Template local pode estar desatualizado')
                
                # Salvar HTML correto
                with open('pontos_bolsao_correto.html', 'w', encoding='utf-8') as f:
                    f.write(html)
                print('\n📄 HTML correto salvo em: pontos_bolsao_correto.html')
                
            else:
                print('❌ Página incorreta carregada')
                
        else:
            print(f'❌ Erro ao acessar pontos_bolsao: {response.status_code}')
            
    else:
        print(f'❌ Erro no login: {login_response.status_code}')
        
except Exception as e:
    print(f'❌ Erro durante o teste: {e}')
