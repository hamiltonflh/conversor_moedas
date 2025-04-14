from flask import Flask, render_template, jsonify
from services.currency_service import CurrencyService
from config.currency_config import options  # Import for rendering the template

app = Flask(__name__)

currency_service = CurrencyService()

@app.route('/')
def index():
    return render_template('index.html', options=options)

@app.route('/cotacao/<moeda1>/<moeda2>/<valor>', methods=['GET'])
def cotacao(moeda1, moeda2, valor):
    result = currency_service.get_conversion_rate(moeda1, moeda2, valor)
    return jsonify(result)

@app.route('/indicadores/<moeda1>/<moeda2>/<int:dias>')
def indicadores(moeda1, moeda2, dias):
    result = currency_service.get_indicators(moeda1, moeda2, dias)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)