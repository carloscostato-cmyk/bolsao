# Configuração de Ambiente de Teste Local

## 🚀 Setup Rápido

### Pré-requisitos
- Python 3.8+
- pip instalado
- Git

### Passo 1: Clonar e Preparar Ambiente
```bash
# Navegar para o diretório do projeto
cd "c:\Users\Carlos Costato\OneDrive - HITSS DO BRASIL SERVIÇOS TECNOLOGICOS LTDA\Documents\Calculadora\sistema_py"

# Criar ambiente virtual (se não existir)
python -m venv .venv

# Ativar ambiente virtual
.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### Passo 2: Iniciar Servidor Local
```bash
# Iniciar servidor Flask
python app.py
```

**Acesso:** http://localhost:5000

### Credenciais de Teste
- **Usuário**: EstratOpera
- **Senha**: Bolsao26

## 🛠️ Scripts de Teste

### Script de Setup Automático
```batch
@echo off
echo Iniciando setup do ambiente de teste...

REM Ativar ambiente virtual
call .venv\Scripts\activate

REM Instalar dependências
echo Instalando dependências...
pip install -r requirements.txt

REM Iniciar servidor
echo Iniciando servidor local...
python app.py

pause
```

### Script de Testes Automatizados
```python
# test_sistema.py
import requests
import time
from datetime import datetime

class SistemaTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_login(self):
        """Testa funcionalidade de login"""
        print("🔍 Testando Login...")
        
        # Tentativa de login inválido
        response = self.session.post(f"{self.base_url}/login", data={
            'usuario': 'invalido',
            'senha': 'invalida'
        })
        assert "Usuário ou senha incorretos" in response.text
        
        # Login válido
        response = self.session.post(f"{self.base_url}/login", data={
            'usuario': 'EstratOpera',
            'senha': 'Bolsao26'
        })
        assert response.status_code == 302  # Redirect
        
        print("✅ Login funcionando corretamente")
        return True
    
    def test_dashboard(self):
        """Testa carregamento do dashboard"""
        print("🔍 Testando Dashboard...")
        
        response = self.session.get(f"{self.base_url}/")
        assert response.status_code == 200
        assert "dashboard" in response.text.lower()
        
        print("✅ Dashboard carregando corretamente")
        return True
    
    def test_pontos_bolsao(self):
        """Testa listagem de pontos bolsão"""
        print("🔍 Testando Pontos Bolsão...")
        
        response = self.session.get(f"{self.base_url}/pontos_bolsao")
        assert response.status_code == 200
        
        print("✅ Listagem de pontos bolsão funcionando")
        return True
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🚀 Iniciando testes automatizados...")
        print("=" * 50)
        
        start_time = time.time()
        
        tests = [
            self.test_login,
            self.test_dashboard,
            self.test_pontos_bolsao
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ {test.__name__} falhou: {e}")
                failed += 1
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("=" * 50)
        print(f"📊 Resultado dos Testes:")
        print(f"✅ Passaram: {passed}")
        print(f"❌ Falharam: {failed}")
        print(f"⏱️ Duração: {duration:.2f}s")
        
        return failed == 0

if __name__ == "__main__":
    tester = SistemaTester()
    success = tester.run_all_tests()
    exit(0 if success else 1)
```

## 📋 Checklist de Validação Local

### ✅ Funcionalidades Básicas
- [ ] Servidor inicia sem erros
- [ ] Login funciona com credenciais corretas
- [ ] Login bloqueia credenciais incorretas
- [ ] Dashboard carrega dados
- [ ] Navegação entre telas funciona

### ✅ Funcionalidades Avançadas
- [ ] Cadastro de novo bolsão
- [ ] Validação de datas
- [ ] Cálculo de pontos
- [ ] Upload de arquivos Excel
- [ ] Conciliação de dados

### ✅ Performance
- [ ] Tempo de resposta < 2s
- [ ] Sem memory leaks
- [ ] Queries executam em < 500ms
- [ ] Interface responsiva

### ✅ Segurança
- [ ] Session management funciona
- [ ] Inputs sanitizados
- [ ] SQL injection prevenido
- [ ] XSS prevenido

## 🔧 Ferramentas de Debug

### Logs do Flask
```python
# Adicionar ao app.py para debug
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Database Inspector
```python
# db_inspector.py
import sqlite3
import os

def inspect_database():
    """Inspecciona o estado atual do banco"""
    DB_PATH = 'sistema.db'
    
    if not os.path.exists(DB_PATH):
        print("❌ Banco de dados não encontrado")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Listar tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("📊 Tabelas encontradas:")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  - {table_name}: {count} registros")
    
    conn.close()

if __name__ == "__main__":
    inspect_database()
```

## 🌐 Acesso Remoto (se necessário)

### Configurar para Acesso Externo
```python
# No final do app.py
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Testar de outros dispositivos
```bash
# Descobrir IP local
ipconfig

# Acessar de outro dispositivo
http://[IP_LOCAL]:5000
```

## 📱 Testes Mobile

### Chrome DevTools
1. Abrir http://localhost:5000
2. F12 → DevTools
3. Toggle device toolbar
4. Testar em diferentes dispositivos

### Testes Manuais Mobile
- [ ] Login em mobile
- [ ] Dashboard responsivo
- [ ] Formulários usáveis
- [ ] Navegação por touch

## 🔍 Monitoramento

### Performance Monitor
```python
# performance_monitor.py
import time
import requests
from datetime import datetime

def monitor_performance(url="http://localhost:5000", duration=60):
    """Monitora performance do sistema"""
    print(f"🔍 Monitorando performance por {duration}s...")
    
    start_time = time.time()
    response_times = []
    
    while time.time() - start_time < duration:
        req_start = time.time()
        try:
            response = requests.get(url, timeout=5)
            req_time = time.time() - req_start
            response_times.append(req_time)
            
            if response.status_code != 200:
                print(f"❌ Status {response.status_code} em {datetime.now()}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        time.sleep(5)
    
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        min_time = min(response_times)
        
        print(f"📊 Performance Summary:")
        print(f"  - Média: {avg_time:.3f}s")
        print(f"  - Máximo: {max_time:.3f}s")
        print(f"  - Mínimo: {min_time:.3f}s")
        print(f"  - Requests: {len(response_times)}")

if __name__ == "__main__":
    monitor_performance()
```

## 🚨 Troubleshooting Comum

### Problema: Servidor não inicia
**Solução:**
```bash
# Verificar se porta está em uso
netstat -ano | findstr :5000

# Matar processo se necessário
taskkill /PID [PID] /F
```

### Problema: Banco de dados corrompido
**Solução:**
```bash
# Restaurar do backup
cp backups/sistema_backup_[mais_recente].db sistema.db
```

### Problema: Dependências faltando
**Solução:**
```bash
# Reinstalar dependências
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

## 📊 Relatório de Testes

### Template de Relatório
```markdown
# Relatório de Testes - [Data]

## Ambiente
- **Sistema**: [Windows/Linux/Mac]
- **Python**: [Versão]
- **Navegador**: [Versão]
- **Data/Hora**: [Timestamp]

## Testes Executados
- [x] Login
- [x] Dashboard
- [x] Pontos Bolsão
- [ ] Novo Bolsão
- [ ] Pontos Utilizados
- [ ] Conciliação

## Issues Encontrados
1. **[Issue]**
   - Severidade: [Alta/Média/Baixa]
   - Descrição: [Detalhes]
   - Passos para reproduzir: [Steps]

## Performance
- Tempo médio resposta: [X.XXXs]
- Requests testados: [N]
- Taxa de sucesso: [XX%]

## Recomendações
1. [Recomendação 1]
2. [Recomendação 2]
```

## 🔄 Workflow de Testes

### Diário
1. Iniciar servidor local
2. Executar testes automatizados
3. Validar funcionalidades críticas
4. Documentar issues

### Semanal
1. Test completo do sistema
2. Testes de performance
3. Testes de segurança
4. Atualizar documentação

### Mensal
1. Testes de carga
2. Testes de stress
3. Validação de backup
4. Relatório completo
