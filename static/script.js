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
                let response = await fetch(`/cotacao/${moedaOrigem}/${moedaDestino}/${valor}`);

                if(!response.ok){
                    let erroData = await response.json()
                    console.log('Erro: ', erroData.erro)
                    return
                } 
                
                let cotmoeda = await response.json();
                document.querySelector('#text-result').innerHTML = `${cotmoeda['valor_convertido']}`;


            } catch (error) {
                console.log("Erro: ", error);
            }
        }

    }  


    input.addEventListener('input', debounce(atualizaConversao, 500));
    moeda1.addEventListener('change', debounce(atualizaConversao,500));
    moeda2.addEventListener('change', debounce(atualizaConversao, 500));
});