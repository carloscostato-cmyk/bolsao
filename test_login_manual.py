import requests
import urllib3

# Desabilitar warnings de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print('🔍 TESTE MANUAL DE LOGIN')
print('=' * 50)

session = requests.Session()

# Tentar diferentes abordagens de login
login_attempts = [
    {
        'url': 'http://localhost:5000/login',
        'data': {'usuario': 'EstratOpera', 'senha': 'Bolsao26'},
        'desc': 'POST direto com dados'
    },
    {
        'url': 'http://localhost:5000/login',
        'data': {'usuario': 'EstratOpera', 'senha': 'Bolsao26', 'submit': 'Login'},
        'desc': 'POST com submit'
    }
]

for i, attempt in enumerate(login_attempts, 1):
    print(f'\n📍 Tentativa {i}: {attempt["desc"]}')
    
    try:
        # Primeiro fazer GET na página de login
        get_response = session.get(attempt['url'])
        print(f'  GET Login: {get_response.status_code}')
        
        # Depois fazer POST
        post_response = session.post(attempt['url'], data=attempt['data'])
        print(f'  POST Login: {post_response.status_code}')
        
        # Verificar redirecionamento
        if post_response.status_code == 302:
            location = post_response.headers.get('Location', '')
            print(f'  ✅ Redirect para: {location}')
            
            # Seguir redirect
            final_response = session.get(f'http://localhost:5000{location}')
            print(f'  Página final: {final_response.status_code}')
            
            if 'Dashboard' in final_response.text:
                print('  ✅ Login bem-sucedido!')
                
                # Agora testar pontos_bolsao
                pontos_response = session.get('http://localhost:5000/pontos_bolsao')
                print(f'  Pontos Bolsão: {pontos_response.status_code}')
                
                if pontos_response.status_code == 200:
                    if 'Catálogo de Pacotes de Pontos' in pontos_response.text:
                        print('  ✅ Página de Pontos Bolsão carregada!')
                        
                        # Contar colunas
                        th_count = pontos_response.text.count('<th>')
                        print(f'  📊 Colunas encontradas: {th_count}')
                        
                        if th_count >= 10:
                            print('  ✅ Template local está CORRETO!')
                        else:
                            print('  ❌ Template local está incompleto')
                            
                        break
                    else:
                        print('  ❌ Página incorreta')
                else:
                    print(f'  ❌ Erro ao acessar pontos_bolsao: {pontos_response.status_code}')
        
        elif post_response.status_code == 200:
            if 'Usuário ou senha incorretos' in post_response.text:
                print('  ❌ Usuário ou senha incorretos')
            else:
                print('  ❌ Login falhou sem mensagem clara')
        else:
            print(f'  ❌ Status inesperado: {post_response.status_code}')
            
    except Exception as e:
        print(f'  ❌ Erro na tentativa: {e}')

print('\n🔍 VERIFICAÇÃO DIRETA DO TEMPLATE')
print('=' * 50)

# Verificar o arquivo template diretamente
try:
    with open('templates/pontos_bolsao.html', 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    th_count = template_content.count('<th>')
    print(f'Colunas <th> no arquivo: {th_count}')
    
    if 'Previsão Início</th>' in template_content:
        print('✅ "Previsão Início" encontrada no template')
    else:
        print('❌ "Previsão Início" NÃO encontrada no template')
        
    if 'Tempo Projeto (meses)</th>' in template_content:
        print('✅ "Tempo Projeto (meses)" encontrada no template')
    else:
        print('❌ "Tempo Projeto (meses)" NÃO encontrada no template')
        
except Exception as e:
    print(f'❌ Erro ao ler template: {e}')
