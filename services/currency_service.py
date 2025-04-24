from config.currency_config import options
from repositories.currency_repository import CurrencyRepository
import statistics
from datetime import datetime
from tzlocal import get_localzone

fuso_horario = get_localzone()

class CurrencyService:
    def __init__(self):
        self.options = options

    def get_conversion_rate(self, moeda1, moeda2, valor):
        valor = float(valor.replace(',', '.'))

        try:
            data = CurrencyRepository.fetch_conversion_rate(moeda1, moeda2)

            if not data.get(f'{moeda1}{moeda2}'):
                return {'erro': 'Moeda Inválida ou não tem cotação hoje'}

            symbol1 = self.options[moeda1]["simbolo"]
            symbol2 = self.options[moeda2]["simbolo"]

            taxa = float(data[f'{moeda1.upper()}{moeda2.upper()}']['ask'])
            valor_convertido = valor * taxa

            return {
                'moeda1': moeda1,
                'moeda2': moeda2,
                'symbol1': symbol1,
                'symbol2': symbol2,
                'valor_original': valor,
                'valor_convertido': round(valor_convertido, 2),
            }
        except Exception as e:
            return {'erro': f'Erro na requisição: {str(e)}'}

    def get_indicators(self, moeda1, moeda2, dias):

        dias = int(dias)
        if dias < 1 or dias > 30:
            return {'erro': 'O número de dias deve ser entre 1 e 30'}
        
        
        if moeda1 == moeda2:
            return {
                'avarageAsk': 0.00,
                'avarageBid': 0.00,
                'spread': 0.00,
                'variation': 0,
                'symbol1' : self.options[moeda1]["simbolo"],
                'symbol2' : self.options[moeda2]["simbolo"],
                'ask': 1.00,
                'date': datetime.now(fuso_horario).strftime('%d-%m-%Y %H:%M:%S UTC %Z%z')
            }

        try:
            data = CurrencyRepository.fetch_historical_data(moeda1, moeda2, dias)

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

            return {
                'moeda1': moeda1,
                'moeda2': moeda2,
                'symbol1': self.options[moeda1]["simbolo"],
                'symbol2': self.options[moeda2]["simbolo"],
                'ask': round(venda, 2),
                'variation': round(variation * 100, 2),
                'avarageAsk': round(float(avarageAsk), 2),
                'avarageBid': round(float(avarageBid), 2),
                'date': date.strftime('%d-%m-%Y %H:%M:%S UTC %Z%z')
            }
        except Exception as e:
            return {'erro': f'Erro na requisição: {str(e)}'}