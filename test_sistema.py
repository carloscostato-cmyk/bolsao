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
