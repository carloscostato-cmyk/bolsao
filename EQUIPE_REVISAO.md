# Equipe de Revisão - Sistema de Pontos Bolsão

## 📋 Visão Geral
Sistema Flask para gestão de pontos do bolsão Fortinet com 7 telas principais:
- Login (`login.html`)
- Dashboard (`index.html`) 
- Pontos Bolsão (`pontos_bolsao.html`)
- Novo Bolsão (`novo_bolsao.html`)
- Pontos Utilizados (`pontos_utilizados.html`)
- Novo Ponto Utilizado (`novo_ponto_utilizado.html`)
- Conciliação (`conciliacao.html`)

## 👥 Papéis e Responsabilidades

### 🎯 Gerente de Projetos
**Responsabilidades:**
- Coordenar toda a equipe de revisão
- Definir cronograma e prioridades
- Garantir alinhamento entre ambiente local vs produção
- Aprovar mudanças críticas
- Reportar status para stakeholders

**Foco Principal:**
- Visão geral do sistema
- Fluxos de negócio completos
- Experiência do usuário (UX)
- Performance geral

### 🔍 Analista Sênior
**Responsabilidades:**
- Revisão técnica profunda do código
- Validação de regras de negócio
- Análise de segurança e autenticação
- Revisão de queries SQL e performance de banco
- Validação de cálculos e lógicas complexas

**Foco Principal:**
- Qualidade do código em `app.py`
- Integridade dos dados
- Validação de inputs e sanitização
- Lógica de cálculo de pontos

### 📊 Analista de Processos
**Responsabilidades:**
- Mapear e validar fluxos de negócio
- Verificar regras de validação em cada tela
- Testar cenários edge case
- Documentar processos atuais vs esperados
- Identificar gaps de processo

**Foco Principal:**
- Fluxo completo de cadastro de bolsão
- Processo de utilização de pontos
- Conciliação entre sistemas
- Validação de datas e valores

### 🧪 Analista de Teste
**Responsabilidades:**
- Executar testes funcionais em todas as telas
- Testar responsividade e UI/UX
- Validar mensagens de erro e sucesso
- Testar integração entre módulos
- Documentar bugs e inconsistências

**Foco Principal:**
- Testes de usabilidade
- Validação visual das telas
- Testes de integração
- Regressão visual

## 📝 Checklist de Revisão por Tela

### 1. Login (`/login`)
- [ ] Validação de usuário/senha
- [ ] Mensagens de erro corretas
- [ ] Redirecionamento pós-login
- [ ] Layout responsivo

### 2. Dashboard (`/`)
- [ ] Cálculos corretos de pontos
- [ ] Exibição de sumários
- [ ] Performance com grandes volumes
- [ ] Visualização clara dos dados

### 3. Pontos Bolsão (`/pontos_bolsao`)
- [ ] Listagem correta dos registros
- [ ] Ordenação adequada
- [ ] Links funcionais
- [ ] Exibição de dados completos

### 4. Novo Bolsão (`/pontos_bolsao/novo`)
- [ ] Validação de todos os campos
- [ ] Lógica de datas (registro < expiração)
- [ ] Validação de anos (2020-2030)
- [ ] Tratamento de erros
- [ ] Limpeza de formulário

### 5. Pontos Utilizados (`/pontos_utilizados`)
- [ ] Cálculo correto de dias consumidos
- [ ] Cálculo de pontos consumidos
- [ ] Exibição de totais e médias
- [ ] Ordenação por data

### 6. Novo Ponto Utilizado (`/pontos_utilizados/novo`)
- [ ] Validação de datas
- [ ] Cálculo de saldo disponível
- [ ] Listagem de bolsões disponíveis
- [ ] Tratamento de erros

### 7. Conciliação (`/conciliacao`)
- [ ] Upload de arquivos Excel
- [ ] Mapeamento correto de colunas
- [ ] Cálculo de diferenças
- [ ] Exibição de status (ok/acima/abaixo)

## 🔄 Processo de Revisão

### Fase 1: Preparação Local
1. Clonar repositório
2. Instalar dependências (`pip install -r requirements.txt`)
3. Iniciar servidor local (`python app.py`)
4. Acessar `http://localhost:5000`

### Fase 2: Revisão Individual
Cada analista executa sua revisão seguindo:
1. Checklist específico do papel
2. Documentação de findings
3. Captura de screenshots
4. Classificação de severidade

### Fase 3: Consolidação
1. Reunião de alinhamento
2. Priorização de issues
3. Definição de plano de ação
4. Atribuição de responsabilidades

### Fase 4: Validação Final
1. Testes de aceitação
2. Validação vs produção
3. Aprovação final
4. Documentação completa

## 📊 Critérios de Avaliação

### Severidade de Issues
- **Crítico**: Quebra sistema ou causa perda de dados
- **Alto**: Impacta funcionalidade principal
- **Médio**: Impacta fluxo secundário
- **Baixo**: Melhoria ou issue cosmético

### Prioridade de Correção
- **P1**: Crítico - Corrigir imediatamente
- **P2**: Alto - Corrigir nesta sprint
- **P3**: Médio - Corrigir próximo ciclo
- **P4**: Baixo - Corrigir quando possível

## 🛠️ Ambiente de Teste

### Configuração Local
```bash
# Instalação
pip install -r requirements.txt

# Execução
python app.py

# Acesso
http://localhost:5000
```

### Credenciais de Teste
- **Usuário**: EstratOpera
- **Senha**: Bolsao26

## 📈 Métricas de Sucesso

### Qualidade
- Zero bugs críticos
- < 5 bugs altos
- 100% cobertura dos fluxos principais

### Performance
- Tempo de resposta < 2s
- Uso de memória adequado
- Sem vazamentos de dados

### Usabilidade
- 100% de telas responsivas
- Navegação intuitiva
- Mensagens claras ao usuário
