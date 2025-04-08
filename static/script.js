document.addEventListener('DOMContentLoaded', function () {
    let input =  document.querySelector('#icurrency');
    let moeda1 = document.querySelector('#imoeda1');
    let moeda2 = document.querySelector('#imoeda2');
   
    function debounce(func, delay) {
        let timer;
        return function(...args) {
            clearTimeout(timer);
            timer = setTimeout(() => func.apply(this, args), delay);
        }
    }


    async function atualizaConversao() {
        let valor = input.value.replace(',', '.');
        let moedaOrigem = moeda1.value;
        let moedaDestino = moeda2.value;

        if(valor && moedaOrigem && moedaDestino) {
            try {
                if(moedaOrigem != moedaDestino){
                    let response = await fetch(`/cotacao/${moedaOrigem}/${moedaDestino}/${valor}`);

                    if(!response.ok){
                        let erroData = await response.json();
                        console.log('Erro: ', erroData.erro);
                        return
                    } 

                    let cotmoeda = await response.json();
                    document.querySelector('#text-result').innerHTML = `${cotmoeda['valor_convertido']}`;
                } else if (moedaOrigem == moedaDestino) {
                    valorfixado = parseFloat(valor).toFixed(2);
                    document.querySelector('#text-result').innerHTML = `${valorfixado}`;
                } else if (input.value == ' '){
                    document.querySelector('#text-result').innerHTML = '00.00';
                }

            } catch (error) {
                console.log("Erro: ", error);
            }
        }

    }  

    async function atualizadash() {
        let moedaOrigem = moeda1.value.replace(',', '.');
        let moedaDestino = moeda2.value.replace(',', '.');
        if(moedaOrigem && moedaDestino) {
            let response = await fetch(`/indicadores/${moedaOrigem}/${moedaDestino}/30`);
            
            if(!response.ok) {
                let erroData = await response.json();
                console.log(erroData.erro);
                return
            }

            let data = await response.json()
            let avarageAsk = data["avarage"];
            let variation = data["variation"];
            document.querySelector('#variation').innerHTML = `${variation}%`
            document.querySelector('#avarage-ask').innerHTML = `${avarageAsk}`;

        }
    }

    //Aplicando a conversão
    input.addEventListener('input', debounce(atualizaConversao, 300));
    moeda1.addEventListener('change', debounce(atualizaConversao,300));
    moeda2.addEventListener('change', debounce(atualizaConversao, 300));

    //Atualização do dashboard
    moeda1.addEventListener('change', debounce(atualizadash, 300));
    moeda2.addEventListener('change', debounce(atualizadash, 300));
    
});