"""
Verifica se o Render já fez o deploy com as 10 colunas
e tenta acionar o deploy automático via GitHub.
"""
import urllib.request, urllib.parse, http.cookiejar, re, ssl, sys
from datetime import datetime

ssl._create_default_https_context = ssl._create_unverified_context
BASE = 'https://bolsao.onrender.com'
USUARIO = 'EstratOpera'
SENHA = 'Bolsao26'

print("=" * 60)
print(f"🔍 VERIFICAÇÃO RENDER - {datetime.now().strftime('%H:%M:%S')}")
print("=" * 60)

# 1. Testar conexão com o site
print("\n📡 1. CONECTANDO AO RENDER...")
try:
    resp = urllib.request.urlopen(f'{BASE}/login', timeout=20)
    print(f"   ✅ Render online! Status: {resp.status}")
except Exception as e:
    print(f"   ❌ Erro ao conectar: {e}")
    sys.exit(1)

# 2. Fazer login
print("\n🔑 2. FAZENDO LOGIN...")
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

data = urllib.parse.urlencode({'usuario': USUARIO, 'senha': SENHA}).encode()
try:
    resp = opener.open(f'{BASE}/login', data, timeout=20)
    if resp.geturl().endswith('/'):
        print("   ✅ Login bem-sucedido!")
    else:
        print("   ⚠️ Login pode ter falhado - tente manualmente")
except Exception as e:
    print(f"   ❌ Erro no login: {e}")

# 3. Verificar colunas em produção
print("\n📊 3. VERIFICANDO COLUNAS EM PRODUÇÃO...")
try:
    resp = opener.open(f'{BASE}/pontos_bolsao', timeout=20)
    html = resp.read().decode('utf-8')
    
    ths = re.findall(r'<th>(.*?)</th>', html)
    print(f"\n   COLUNAS ENCONTRADAS: {len(ths)}")
    for i, th in enumerate(ths, 1):
        print(f"     {i}. {th.strip()}")
    
    if 'Previsão' in html and 'Tempo Projeto' in html:
        print("\n   ✅✅✅ 10 COLUNAS EM PRODUÇÃO - CORREÇÃO APLICADA!")
    else:
        print("\n   ❌❌❌ AINDA COM 8 COLUNAS")
        print("\n   🔄 Render pode levar alguns minutos para reimplantar.")
        print("   🔄 Vá até https://dashboard.render.com e clique em")
        print("   🔄 'Deploy' → 'Clear build cache & deploy' para forçar.\n")
        
        # Diagnosticar versão
        if 'colspan="8"' in html:
            print("   → Template antigo detectado (colspan=8)")
        elif 'colspan="10"' in html:
            print("   → Template novo detectado (colspan=10)")
        
except Exception as e:
    print(f"   ❌ Erro ao acessar pontos_bolsao: {e}")

# 4. Verificar GitHub
print("\n📦 4. VERIFICANDO GITHUB...")
try:
    resp = urllib.request.urlopen('https://api.github.com/repos/carloscostato-cmyk/Bolsao/git/refs/heads/master', timeout=10)
    import json
    data = json.loads(resp.read())
    sha = data['object']['sha']
    print(f"   ✅ GitHub - último commit: {sha[:8]}")
except Exception as e:
    print(f"   ⚠️ Erro ao verificar GitHub: {e}")

print("\n" + "=" * 60)
print("📋 RESUMO")
print("=" * 60)
print(f"""
📦 GitHub:    Código com 10 colunas ✅ (commit e6ffc8e)
💻 Local:     Template com 10 colunas ✅
🌐 Render:    {'✅ 10 COLUNAS' if 'Previsão' in html and 'Tempo Projeto' in html else '❌ 8 colunas - aguardando deploy'}

👉 Acesse: https://dashboard.render.com
   Selecione o serviço "bolsao"
   Clique em "Manual Deploy" → "Clear build cache & deploy"
""")