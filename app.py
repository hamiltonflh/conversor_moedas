from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
from tzlocal import get_localzone
import statistics

app = Flask(__name__)

fuso_horario = get_localzone()


options = {
    'BRL' : {'nome': 'Real Brasileiro', 'simbolo': 'R$'},
    'USD' : {'nome' : 'Dolar Americano', 'simbolo' : 'US$'},
    'EUR' : {'nome' : 'Euro', 'simbolo' : '€'},
    'GBP' : {'nome' : 'Libra Esterlina', 'simbolo' : '£'},
    'JPY' : {'nome' : 'Iene Japonês', 'simbolo' : '¥'},
    'CHF' : {'nome' : 'Franco Suíço', 'simbolo' : 'CHF'},
    'CAD' : {'nome' : 'Dólar Canadense', 'simbolo' : 'C$'},
    'AUD' : {'nome' : 'Dólar Australiano', 'simbolo' : 'A$'},
    'ARS' : {'nome' : 'Peso Argentino', 'simbolo' : '$'},
    'MXN' : {'nome' : 'Peso Mexicano', 'simbolo' : '$'},
    'RUB' : {'nome' : 'Rublo Russo', 'simbolo' : '₽'},
    'INR' : {'nome' : 'Rupia Indiana', 'simbolo' : '₹'},
    'ZAR' : {'nome' : 'Rand Sul-Africano', 'simbolo' : 'R'},
    'KRW' : {'nome' : 'Won Sul-Coreano', 'simbolo' : '₩'},
    'CNY' : {'nome' : 'Yuan Chinês', 'simbolo' : '¥'}
}



@app.route('/')
def index():
    return render_template('index.html', options = options)


@app.route('/cotacao/<moeda1>/<moeda2>/<valor>', methods=['GET'])
def cotacao(moeda1, moeda2, valor):
    valor = float(valor.replace(',', '.'))

    api = f"https://economia.awesomeapi.com.br/json/last/{moeda1.upper()}-{moeda2.upper()}"
        
    try:
        response = requests.get(api)
        data = response.json()

        if not data.get(f'{moeda1}{moeda2}'):
            return jsonify({'erro': 'Moeda Inválida ou não tem cotação hoje'})
        
        symbol1 = options[moeda1]["simbolo"]
        symbol2 = options[moeda2]["simbolo"]

        taxa = float(data[f'{moeda1.upper()}{moeda2.upper()}']['ask'])
        valor_convertido = valor * taxa

        return  jsonify({
            'moeda1': moeda1,
            'moeda2': moeda2,
            'symbol1' : symbol1,
            'symbol2' : symbol2,
            'valor_original': valor,
            'valor_convertido': round(valor_convertido, 2),
        })

    except Exception as e:
        return jsonify({'erro': f'Erro na requisição: {str(e)}'})


@app.route('/indicadores/<moeda1>/<moeda2>/<int:dias>')
def indicadores(moeda1, moeda2, dias):
    try:
        if moeda1 == moeda2:
            avarageAsk = float(0.00)
            avarageBid = float(0.00)
            spread = 0.00
            variation = 0
            venda = 1.00
            date = datetime.now(fuso_horario)
        else: 
            api = f"https://economia.awesomeapi.com.br/json/daily/{moeda1.upper()}-{moeda2.upper()}/{dias}"

            response = requests.get(api)
            data = response.json()
            
            symbol1 = options[moeda1]["simbolo"]
            symbol2 = options[moeda2]["simbolo"]


            ask_values = [float(item.get("ask", 0)) for item in data]
            bid_values = [float(item.get("bid", 0)) for item in data]
            var_values = [float(item.get("pctChange", 0)) for item in data]

            avarageAsk = statistics.mean(ask_values)
            avarageBid = statistics.mean(bid_values)
            variation = statistics.mean(var_values)
            venda = float(data[0]['ask'])
            compra = float(data[0]['bid'])

            spread = (venda - compra) / compra

            timestamp = int(data[0]['timestamp'])
            date = datetime.fromtimestamp(timestamp, fuso_horario)
        return jsonify({
            'moeda1': moeda1,
            'moeda2': moeda2,
            'symbol1' : symbol1,
            'symbol2' : symbol2,
            'ask' : round(venda,2),
            'variation' : round(variation * 100,2),
            'avarageAsk' : round(float(avarageAsk), 2),
            'avarageBid' : round(float(avarageBid), 2),
            'spread' : round(float(spread) * 100, 2),
            'date' : date.strftime('%d-%m-%Y %H:%M:%S UTC %Z%z')

        })
    
    except Exception as e:
        return jsonify({'erro': f'Erro na requisição: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)