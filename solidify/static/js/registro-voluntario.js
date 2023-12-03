document.getElementById('volunt_cpf').addEventListener('keydown', function(event) {
    if (event.key === 'Backspace' || event.key === 'Delete' || event.key === 'Tab' || event.key === 'Escape' || event.key === 'Enter' || event.key === 'v' && (event.ctrlKey || event.metaKey)) {
        return;
    }

    if (isNaN(Number(event.key))) {
        event.preventDefault();
    }
});

document.getElementById('volunt_cpf').addEventListener('input', function(event) {
    let inputValue = event.target.value;

    let cpf = inputValue.replace(/\D/g, '');

    cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
    cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
    cpf = cpf.replace(/(\d{3})(\d{1,2})$/, '$1-$2');

    // Atualiza o valor no campo de input
    event.target.value = cpf;
});

document.getElementById('voluntarioForm').addEventListener('submit', (e) => {
    e.preventDefault();

    var spans = document.querySelectorAll('span');
    spans.forEach(function(span) {
        var paragrafos = span.querySelectorAll('p');
        paragrafos.forEach(function(paragrafo) {
            span.removeChild(paragrafo);
        });
    });

    var cpf = document.getElementById('volunt_cpf').value;
    var email = document.getElementById('volunt_email').value;

    var url = "/validar/usuario/";

    fetch(`${url}?cpf=${cpf}&email=${email}`)
            .then(response => response.json())
            .then(data => {
                if (data.valido === false) {
                    if (Array.isArray(data.erros) && data.erros.length > 0) {
                        data.erros.forEach(erro => {
                            var isValido = erro.valido;
                            var itemInvalido = erro.itemInvalido;
                            var mensagem = erro.mensagem;
                            var msgErro = document.getElementById(itemInvalido)

                            msgErro.innerHTML += `<p>${mensagem}</p>`;
                        });
                    }
                } else {
                     e.target.submit();
                }
            })
})

/*---------------------------------------------------------------------*/

document.getElementById('volunt_cep').addEventListener('keydown', (event) =>  {
    const cepInput = event.target;
    const key = event.key;

    if (event.key === 'Backspace' || event.key === 'Delete' || event.key === 'Tab' || event.key === 'Escape' || event.key === 'Enter' || event.key === 'v' && (event.ctrlKey || event.metaKey)) {
        return;
    }

    if (!isAllowedKey) {
        event.preventDefault();
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
document.getElementById('volunt_cep').addEventListener('focusout', (e) => buscarPreencheEndereco(e));

function buscarPreencheEndereco(e) {
    e.preventDefault();

    var cep = document.getElementById('volunt_cep').value;

    if(cep && cep.length === 9) {
        var url = '/endereco/';

        fetch(`${url}?cep=${cep}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('volunt_endereco').value = data.endereco;
                document.getElementById('volunt_bairro').value = data.bairro;
                document.getElementById('volunt_cidade').value = data.cidade;
                document.getElementById('volunt_uf').value = data.uf;
            })
            .catch(error => {
                console.error('Ocorreu um erro:', error);
            });
    }
}