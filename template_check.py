from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

@app.route('/check-template')
def check_template():
    """Verificar template diretamente"""
    
    pontos = []  # Dados vazios como no sistema real
    
    try:
        # Ler template diretamente do arquivo
        template_path = os.path.join('templates', 'pontos_bolsao.html')
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        print('🔍 VERIFICAÇÃO DIRETA DO ARQUIVO TEMPLATE')
        print('=' * 60)
        
        # Verificar se as colunas estão no arquivo
        checks = [
            ('Previsão Início</th>', 'Coluna Previsão Início no <th>'),
            ('Tempo Projeto (meses)</th>', 'Coluna Tempo Projeto no <th>'),
            ('previsao_inicio', 'Campo previsao_inicio no código'),
            ('tempo_projeto_meses', 'Campo tempo_projeto_meses no código'),
            ('colspan="10"', 'Colspan correto para 10 colunas')
        ]
        
        print('Verificação do arquivo pontos_bolsao.html:')
        for check, description in checks:
            if check in template_content:
                print(f'  ✅ {description}')
            else:
                print(f'  ❌ {description}')
        
        # Contar colunas <th>
        th_count = template_content.count('<th>')
        print(f'\n📊 Total de colunas <th> encontradas: {th_count}')
        
        if th_count >= 10:
            print('✅ Template parece ter todas as colunas necessárias')
        else:
            print('❌ Template pode estar faltando colunas')
        
        # Verificar se há dados de exemplo
        if '{% for ponto in pontos %}' in template_content:
            print('✅ Estrutura de loop presente')
        else:
            print('❌ Estrutura de loop ausente')
        
        # Renderizar template para teste
        html_renderizado = render_template('pontos_bolsao.html', pontos=pontos)
        
        print('\n🔍 VERIFICAÇÃO DO HTML RENDERIZADO')
        print('=' * 60)
        
        # Verificar colunas no HTML final
        for check, description in checks[:2]:  # Apenas as colunas visuais
            if check in html_renderizado:
                print(f'  ✅ {description} - Presente no render')
            else:
                print(f'  ❌ {description} - Ausente no render')
        
        return html_renderizado
        
    except Exception as e:
        print(f'❌ Erro na verificação: {e}')
        return f'Erro: {e}'

if __name__ == '__main__':
    app.run(debug=True, port=5002)
