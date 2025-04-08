from flask import Flask, request, render_template, jsonify
import requests
from datetime import datetime, timedelta
import statistics

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cotacao/<moeda1>/<moeda2>/<valor>', methods=['GET'])
def cotacao(moeda1, moeda2, valor):
    valor = float(valor.replace(',', '.'))

    api = f"https://economia.awesomeapi.com.br/json/last/{moeda1.upper()}-{moeda2.upper()}"
        
    try:
        response = requests.get(api)
        data = response.json()

        if not data.get(f'{moeda1}{moeda2}'):
            return jsonify({'erro': 'Moeda Inválida ou não tem cotação hoje'})
        
        taxa = float(data[f'{moeda1.upper()}{moeda2.upper()}']['ask'])
        valor_convertido = valor * taxa

        return  jsonify({
            'moeda1': moeda1,
            'moeda2': moeda2,
            'valor_original': valor,
            'valor_convertido': round(valor_convertido, 2),
        })

    except Exception as e:
        return jsonify({'erro': f'Erro na requisição: {str(e)}'})


@app.route('/indicadores/<moeda1>/<moeda2>/<int:dias>')
def indicadores(moeda1, moeda2, dias):
    try:
        api = f"https://economia.awesomeapi.com.br/json/daily/{moeda1.upper()}-{moeda2.upper()}/{dias}"

        response = requests.get(api)
        data = response.json()
        ask_values = [float(item.get("ask", 0)) for item in data]
        var_values = [float(item.get("pctChange", 0)) for item in data]

        avarage = statistics.mean(ask_values)
        variation = statistics.mean(var_values) 
        

        return jsonify({
            'moeda1': moeda1,
            'moeda2': moeda2,
            'variation' : round(variation * 100,2),
            'avarage' : round(avarage, 2)
        })
    
    except Exception as e:
        return jsonify({'erro': f'Erro na requisição: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)