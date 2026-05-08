# 🚀 Guia Rápido para Equipe de Revisão

## 📋 Visão Geral do Projeto
**Sistema:** Gestão de Pontos Bolsão Fortinet  
**Tecnologia:** Flask + SQLite + HTML/CSS/JavaScript  
**Telas:** 7 telas principais  
**Objetivo:** Comparar ambiente local vs produção e identificar diferenças

## 👥 Sua Equipe
- **🎯 Gerente de Projetos:** Coordenação geral e stakeholders
- **🔍 Analista Sênior:** Revisão técnica e qualidade de código
- **📊 Analista de Processos:** Fluxos de negócio e regras
- **🧪 Analista de Teste:** Usabilidade e validação funcional

## 🚀 Setup Inicial (5 minutos)

### 1. Preparar Ambiente
```bash
# Navegar para o projeto
cd "c:\Users\Carlos Costato\OneDrive - HITSS DO BRASIL SERVIÇOS TECNOLOGICOS LTDA\Documents\Calculadora\sistema_py"

# Ativar ambiente virtual
.venv\Scripts\activate

# Instalar dependências (se necessário)
pip install -r requirements.txt
```

### 2. Iniciar Servidor Local
```bash
python app.py
```

### 3. Acessar Sistema
**URL:** http://localhost:5000  
**Usuário:** EstratOpera  
**Senha:** Bolsao26

## 📱 Telas para Revisar

### 1. Login (`/login`)
- **Foco:** Validação de credenciais e mensagens de erro
- **Teste:** Tentar login inválido, depois válido

### 2. Dashboard (`/`)
- **Foco:** Cálculos de pontos e exibição de sumários
- **Teste:** Verificar se valores fazem sentido

### 3. Pontos Bolsão (`/pontos_bolsao`)
- **Foco:** Listagem e ordenação de registros
- **Teste:** Navegar pela listagem

### 4. Novo Bolsão (`/pontos_bolsao/novo`)
- **Foco:** Validação de formulário e regras de data
- **Teste:** Tentar cadastrar com datas inválidas

### 5. Pontos Utilizados (`/pontos_utilizados`)
- **Foco:** Cálculo de dias e pontos consumidos
- **Teste:** Verificar cálculos matemáticos

### 6. Novo Ponto Utilizado (`/pontos_utilizados/novo`)
- **Foco:** Seleção de bolsão e validação
- **Teste:** Tentar cadastrar novo ponto

### 7. Conciliação (`/conciliacao`)
- **Foco:** Upload de Excel e cálculo de diferenças
- **Teste:** Fazer upload de arquivo (se disponível)

## 🔍 Checklist Rápido por Papel

### 🎯 Gerente de Projetos
- [ ] Sistema inicia sem erros?
- [ ] Todas as telas carregam?
- [ ] Performance aceitável (< 3s)?
- [ ] Experiência do usuário é boa?

### 🔍 Analista Sênior
- [ ] Código está organizado?
- [ ] Queries SQL estão otimizadas?
- [ ] Validações de input são seguras?
- [ ] Cálculos matemáticos estão corretos?

### 📊 Analista de Processos
- [ ] Fluxo de negócio faz sentido?
- [ ] Validações são adequadas?
- [ ] Regras de data estão corretas?
- [ ] Processo é intuitivo?

### 🧪 Analista de Teste
- [ ] Interface é responsiva?
- [ ] Mensagens são claras?
- [ ] Navegação é intuitiva?
- [ ] Não há bugs visuais?

## 📊 Como Documentar Issues

### Template Rápido
```
Issue #001 - [Título curto]
Severidade: [Crítico/Alto/Médio/Baixo]
Tela: [Nome da tela]
Descrição: [O que está errado?]
Passos: [1. Fazer isso, 2. Fazer aquilo]
Evidência: [Screenshot ou descrição]
```

### Onde Documentar
- **Urgente:** Slack/Teams imediatamente
- **Formal:** Arquivo `docs/issues/` com nome padrão
- **Discussão:** Reunião diária às 9:00 AM

## 🔄 Workflow Diário

### Manhã (9:00 AM - 10:00 AM)
1. **Setup:** Iniciar servidor local
2. **Alinhamento:** Reunião rápida 15 min
3. **Testes:** Cada um foca em suas telas
4. **Documentar:** Registrar issues encontradas

### Tarde (4:00 PM - 5:00 PM)
1. **Consolidação:** Juntar todos os feedbacks
2. **Priorização:** Classificar issues por severidade
3. **Planejamento:** Definir próximos passos
4. **Comunicação:** Reportar status

## 🚨 O que Fazer se...

### Servidor não inicia?
```bash
# Verificar se porta está ocupada
netstat -ano | findstr :5000

# Matar processo se necessário
taskkill /PID [PID] /F

# Tentar novamente
python app.py
```

### Esqueci a senha?
- **Usuário:** EstratOpera
- **Senha:** Bolsao26

### Banco de dados está vazio?
- Verifique arquivo `sistema.db`
- Restaure do backup em `backups/`

### Encontrei um bug crítico?
1. **Pare tudo** e documente imediatamente
2. **Tire screenshot** se possível
3. **Reporte** no Slack/Teams
4. **Não continue** testes até avaliação

## 📈 Métricas de Sucesso

### Diariamente
- **Telas revisadas:** Meta 7/7
- **Issues críticas:** Meta 0
- **Issues altas:** Meta < 3
- **Documentação:** 100% das issues

### Semanalmente
- **Coverage:** 100% dos fluxos testados
- **Performance:** < 2s tempo médio
- **Qualidade:** < 5 bugs totais
- **Satisfação:** Feedback positivo

## 📁 Arquivos Importantes

### Para Ler Agora
- `EQUIPE_REVISAO.md` - Detalhes dos papéis
- `CHECKLIST_COMPARACAO.md` - Comparação local vs produção
- `AMBIENTE_TESTE.md` - Setup e troubleshooting

### Para Usar Durante Testes
- `test_sistema.py` - Testes automatizados
- `PROCESSO_FEEDBACK.md` - Como documentar

## 🎯 Objetivos Finais

### Imediatos (Hoje)
1. **Setup** do ambiente local para todos
2. **Revisão** inicial das 7 telas
3. **Identificação** de issues críticas
4. **Documentação** dos primeiros findings

### Curto Prazo (Esta Semana)
1. **Comparação** sistemática local vs produção
2. **Priorização** de issues por impacto
3. **Plano** de correção dos problemas
4. **Validação** das soluções propostas

### Médio Prazo (Próxima Semana)
1. **Implementação** das correções
2. **Testes** de regressão
3. **Documentação** final
4. **Apresentação** dos resultados

## 🆘 Suporte

### Contato Imediato
- **Gerente:** [Contato do gerente]
- **Analista Sênior:** [Contato técnico]
- **Slack/Teams:** #revisao-sistema

### Recursos
- **Documentação:** Pasta `docs/`
- **Templates:** Vários arquivos .md
- **Scripts:** `test_sistema.py`

## 🏆 Reconhecimento

### Como Ser Reconhecido
- **Proatividade:** Identificar issues antes dos outros
- **Qualidade:** Documentação detalhada e clara
- **Colaboração:** Ajudar outros membros da equipe
- **Iniciativa:** Sugerir melhorias no processo

### Celebrar Conquistas
- **Zero bugs críticos** em um dia
- **Issue complexa** resolvida
- **Melhoria** significativa no processo
- **Feedback** positivo do usuário final

---

## 🚀 Comece Agora!

1. **Leia** os arquivos de documentação
2. **Setup** seu ambiente local
3. **Inicie** os testes conforme seu papel
4. **Documente** tudo o que encontrar
5. **Comunique** issues críticas imediatamente

**Lembre-se:** O objetivo é garantir que o ambiente local seja idêntico ao de produção. Cada detalhe importa!

**Boa sorte, equipe! 🎯**
