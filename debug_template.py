import requests
from flask import Flask, render_template
import sqlite3
import os

# Criar app Flask para testar template diretamente
app = Flask(__name__)

@app.route('/test-template')
def test_template():
    """Testar renderização direta do template"""
    
    # Simular dados vazios como no sistema real
    pontos = []
    
    try:
        # Renderizar template diretamente
        html_renderizado = render_template('pontos_bolsao.html', pontos=pontos)
        
        print('🔍 ANÁLISE DO TEMPLATE RENDERIZADO')
        print('=' * 50)
        
        # Verificar se as colunas estão no HTML renderizado
        colunas_esperadas = [
            'Previsão Início',
            'Tempo Projeto (meses)',
            'Previsão Início</th>',
            'Tempo Projeto (meses)</th>'
        ]
        
        print('Verificação de colunas no HTML renderizado:')
        for coluna in colunas_esperadas:
            if coluna in html_renderizado:
                print(f'  ✅ Encontrado: {coluna}')
            else:
                print(f'  ❌ Não encontrado: {coluna}')
        
        # Verificar estrutura da tabela
        if '<th>Previsão Início</th>' in html_renderizado:
            print('\n✅ Coluna "Previsão Início" encontrada no <th>')
        else:
            print('\n❌ Coluna "Previsão Início" NÃO encontrada no <th>')
            
        if '<th>Tempo Projeto (meses)</th>' in html_renderizado:
            print('✅ Coluna "Tempo Projeto (meses)" encontrada no <th>')
        else:
            print('❌ Coluna "Tempo Projeto (meses)" NÃO encontrada no <th>')
        
        # Salvar HTML para inspeção
        with open('debug_template_output.html', 'w', encoding='utf-8') as f:
            f.write(html_renderizado)
        
        print('\n📄 HTML renderizado salvo em: debug_template_output.html')
        
        return html_renderizado
        
    except Exception as e:
        print(f'❌ Erro ao renderizar template: {e}')
        return f'Erro: {e}'

if __name__ == '__main__':
    app.run(debug=True, port=5001)
