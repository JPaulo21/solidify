document.getElementById('idOngCnpj').addEventListener('keydown', (event) => {
  if (event.key === 'Backspace' || event.key === 'Delete' || event.key === 'Tab' || event.key === 'Escape' || event.key === 'Enter' || event.key === 'v' && (event.ctrlKey || event.metaKey)) {
    return;
  }

  if (isNaN(Number(event.key))) {
    event.preventDefault();
  }

  setTimeout(() => {
    cnpjInput = document.getElementById('idOngCnpj');
    let cnpj = cnpjInput.value.replace(/\D/g, '');
    cnpj = cnpj.substring(0, 14);

    cnpj = cnpj.replace(/^(\d{2})(\d)/, '$1.$2');
    cnpj = cnpj.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
    cnpj = cnpj.replace(/^(\d{2})\.(\d{3})\.(\d{3})(\d)/, '$1.$2.$3/$4');
    cnpj = cnpj.replace(/^(\d{2})\.(\d{3})\.(\d{3})\/(\d{4})(\d)/, '$1.$2.$3/$4-$5');

    cnpjInput.value = cnpj;
  }, 0);
});

/*--------------------------*/

document.getElementById('idOngCEP').addEventListener('keydown', (e) =>  {
    const cepInput = e.target;
    const key = e.key;

    const isAllowedKey = /^\d$/.test(key) || ['Backspace', 'Delete', 'Tab', 'Escape', 'Enter', 'Control', 'v'].includes(key);
    
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
document.getElementById('idOngCEP').addEventListener('focusout', (e) => buscarPreencheEndereco(e));

function buscarPreencheEndereco(e) {
    e.preventDefault();

    var cep = document.getElementById('idOngCEP').value;

    if(cep && cep.length === 9) {
        var url = '/endereco/';

        fetch(`${url}?cep=${cep}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('idOngEndereco').value = data.endereco;
                document.getElementById('idOngBairro').value = data.bairro;
                document.getElementById('idOngCidade').value = data.cidade;
                document.getElementById('idOngUF').value = data.uf;
            })
            .catch(error => {
                console.error('Ocorreu um erro:', error);
            });
    }
}

document.getElementById('idAdmCPF').addEventListener('keydown', function(event) {
  if (event.key === 'Backspace' || event.key === 'Delete' || event.key === 'Tab' || event.key === 'Escape' || event.key === 'Enter' || event.key === 'v' && (event.ctrlKey || event.metaKey)) {
    return;
  }

  if (isNaN(Number(event.key))) {
    event.preventDefault();
  }
});

document.getElementById('idAdmCPF').addEventListener('input', function(event) {
    let inputValue = event.target.value;

    // Remove qualquer caractere que não seja número
    let cpf = inputValue.replace(/\D/g, '');

    // Aplica a formatação do CPF
    cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
    cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
    cpf = cpf.replace(/(\d{3})(\d{1,2})$/, '$1-$2');

    // Atualiza o valor no campo de input
    event.target.value = cpf;
});

/*-------------------------------------------------------------------------------------*/

document.getElementById('voluntarioForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    var spans = document.querySelectorAll('span');
    spans.forEach(function(span) {
        var paragrafos = span.querySelectorAll('p');
        paragrafos.forEach(function(paragrafo) {
            span.removeChild(paragrafo);
        });
    });

    var usuarioValido = '';
    var ongValida = '';

    var cpf = document.getElementById('idAdmCPF').value;
    var email = document.getElementById('idAdmEmail').value;

    var urlU = "/validar/usuario/";

    await fetch(`${urlU}?cpf=${cpf}&email=${email}`)
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
                    console.log(`USUARIO usuarioValida: ${usuarioValido} e data.valido: ${data.valido}`)
                    usuarioValido = data.valido;
                }
            })

    var cnpj = document.getElementById('idOngCnpj').value;

    var url = "/validar/ong/";

    await fetch(`${url}?cnpj=${cnpj}`)
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
                    console.log(`CNPJ ongValida: ${ongValida} e data.valido: ${data.valido}`)
                     ongValida = data.valido;
                }
            })

    console.log(`FORA ongValida: ${ongValida} e usuarioValido: ${usuarioValido}`);
    if(ongValida && usuarioValido){
        console.log(`DENTRO ongValida: ${ongValida} e usuarioValido: ${usuarioValido}`);
        e.target.submit();
    }
})