
const prox = document.getElementById("proximo")
prox.addEventListener("click", (e) => {
    prox.style.display = "none";
    const dados_eventos = document.getElementsByClassName("dados-eventos")
    dados_eventos[0].style.display = "none"

    const anterior = document.getElementsByClassName("anterior")
    anterior[0].style.display = ""

    const vagas = document.getElementsByClassName("vagas")
    vagas[0].style.display = ""
})

const anterior = document.getElementById("anterior")
anterior.addEventListener("click", (e) => {
    anterior.style.display = "none";
    const vagas = document.getElementsByClassName("vagas")
    vagas[0].style.display = "none"

    const prox = document.getElementsByClassName("proximo")
    prox[0].style.display = ""

    const dados_eventos = document.getElementsByClassName("dados-eventos")
    dados_eventos[0].style.display = ""
})

/*-----------------------------------------------------------------------*/

document.getElementById('numero').addEventListener('keydown', function(event) {
  // Permite: backspace, delete, tab, escape, enter
  if (event.key === 'Backspace' || event.key === 'Delete' || event.key === 'Tab' || event.key === 'Escape' || event.key === 'Enter') {
    return;
  }

  if (isNaN(Number(event.key))) {
    event.preventDefault();
  }
});

/*---------------------------------------------------*/

document.getElementById('addCargo').addEventListener('click', (e) => {
    var numero = document.getElementById('numero').value;
    var cargo = document.getElementById('cargo').value;
    var tbody = document.querySelector('tbody');

    if (numero && cargo){
        var newRow = document.createElement('tr');
        var cargoCell = document.createElement('td');
        cargoCell.textContent = cargo;
        var numeroCell = document.createElement('td');
        numeroCell.textContent = numero;

        var hiddenInputNumero = document.createElement('input');
        hiddenInputNumero.type = 'hidden';
        hiddenInputNumero.name = 'numeros[]';
        hiddenInputNumero.value = numero;

        var hiddenInputCargo = document.createElement('input');
        hiddenInputCargo.type = 'hidden';
        hiddenInputCargo.name = 'cargos[]';
        hiddenInputCargo.value = cargo;

        newRow.appendChild(cargoCell);
        newRow.appendChild(numeroCell);
        newRow.appendChild(hiddenInputCargo)
        newRow.appendChild(hiddenInputNumero)
        tbody.appendChild(newRow);

        let totalItems = parseInt(document.getElementById('total').textContent);
        let valorNumeroCell = parseInt(numero);
        totalItems += isNaN(valorNumeroCell) ? 0 : valorNumeroCell;

        document.getElementById('total').textContent = totalItems;
        document.getElementById('input-total').value  = parseInt(totalItems)

        document.getElementById('numero').value = ''
        document.getElementById('cargo').value = ''
    }
 });

 /*-----------------------------------------------------------------*/

document.getElementById('evento_cep').addEventListener('keydown', (e) =>  {
    const cepInput = e.target;
    const key = e.key;

    const isAllowedKey = /^\d$/.test(key) || ['Backspace', 'Delete', 'Tab', 'Escape', 'Enter'].includes(key);

    if (!isAllowedKey) {
        e.preventDefault();
        return;
    }

    let cep = cepInput.value.replace(/\D/g, '');

    if (cep.length <= 5 && key != 'Backspace') {
        cepInput.value = cep.replace(/^(\d{5})/, '$1-');
    } else if (key == 'Backspace') {
        cep = cep.substring(0, nextCharIndex - 1) + cep.substring(nextCharIndex + 1);
        cepInput.value = cep.replace(/^(\d{5})(\d{0,3})/, '$1-$2').substring(0, 9);
        cepInput.setSelectionRange(nextCharIndex - 1, nextCharIndex - 1);
    } else {
        cep = cep.replace(/^(\d{5})(\d{0,3}).*/, '$1-$2');
    }

});

document.getElementById('pesquisarEndereco').addEventListener('click', (e) => buscarPreencheEndereco(e));
document.getElementById('evento_cep').addEventListener('focusout', (e) => buscarPreencheEndereco(e));

function  buscarPreencheEndereco(e) {
    e.preventDefault();

    var cep = document.getElementById('evento_cep').value;

    if(cep && cep.length === 9) {
        var url = '/endereco/';

        fetch(`${url}?cep=${cep}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('evento_endereco').value = data.endereco;
                document.getElementById('evento_bairro').value = data.bairro;
                document.getElementById('evento_cidade').value = data.cidade;
                document.getElementById('evento_uf').value = data.uf;
            })
            .catch(error => {
                console.error('Ocorreu um erro:', error);
            });
    }
}