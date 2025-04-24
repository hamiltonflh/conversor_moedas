# Conversor de Moedas

Este projeto é um **Conversor de Moedas** que permite a conversão de valores entre diferentes moedas e a exibição de indicadores financeiros, como média de cotação, variação e spread, utilizando dados de uma API externa.

## Funcionalidades

- **Conversão de Moedas**: Converta valores entre diferentes moedas com base na taxa de câmbio atual.
- **Indicadores Financeiros**:
  - Média de cotação (ask e bid) nos últimos dias.
  - Variação percentual média.
- **Validação de Dados**: Verificação de moedas válidas e intervalo de dias permitido (1 a 30).

## Estrutura do Projeto
conversor_moedas/ 
    ├── app.py # Arquivo principal da aplicação 
        ├── config/ 
            └── currency_config.py # Configuração das moedas disponíveis 
        ├── repositories/
            └── currency_repository.py # Repositório para comunicação com a API externa 
        ├── services/
            └── currency_service.py # Lógica de negócios para conversão e indicadores 
        ├── templates/
            ├── index.html # Página principal │ 
            └── layout.html # Layout base
        ├── static/
            ├── style.css # Estilos CSS
            └── script.js # Lógica do frontend 
    ├── requirements.txt # Dependências do projeto 
    └── README.md # Documentação do projeto

## Tecnologias Utilizadas

- **Python 3.10**
- **Flask**: Framework web para Python.
- **Bootstrap**: Framework CSS para design responsivo.
- **AwesomeAPI**: API externa para obter dados de câmbio.
- **tzlocal**: Para lidar com fusos horários locais.
- **statistics**: Biblioteca padrão do Python para cálculos estatísticos.

## Instalação e Execução

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/conversor-moedas.git
   cd conversor-moedas
   
2.Crie um ambiente virtual e ative-o:
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate

3.Instale as dependências:
    pip install -r requirements.txt


4.Execute o servidor:
    python app.py

5.Acesse a aplicação no navegador:
    http://127.0.0.1:5000/


## Testes
    Para executar os testes unitários, use o comando:
    python -m unittest discover

## Endpoints Principais

# Conversão de Moedas:
    Endpoint: /convert
    Parâmetros:
        moeda1: Código da moeda de origem (ex.: USD).
        moeda2: Código da moeda de destino (ex.: BRL).
        valor: Valor a ser convertido.
# Resposta:
{
  "moeda1": "USD",
  "moeda2": "BRL",
  "symbol1": "$",
  "symbol2": "R$",
  "valor_original": 100.0,
  "valor_convertido": 500.0
}

# Indicadores Financeiros
    Endpoint: /indicators
    Parâmetros:
        moeda1: Código da moeda de origem.
        moeda2: Código da moeda de destino.
        dias: Número de dias para cálculo dos indicadores (1 a 30).
        Resposta:
        {
            "moeda1": "USD",
            "moeda2": "BRL",
            "symbol1": "$",
            "symbol2": "R$",
            "ask": 5.0,
            "variation": 0.5,
            "avarageAsk": 5.1,
            "avarageBid": 4.9,
            "date": "24-04-2025 12:00:00 UTC -0300"
        }
        
## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença
Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.