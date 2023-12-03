document.getElementById('idCPF').addEventListener('keydown', function(event) {
  if (event.key === 'Backspace' || event.key === 'Delete' || event.key === 'Tab' || event.key === 'Escape' || event.key === 'Enter' || event.key === 'v' && (event.ctrlKey || event.metaKey)) {
    return;
  }

});

document.getElementById('idCPF').addEventListener('input', function(event) {
    let inputValue = event.target.value;
    let cpf = inputValue.replace(/\D/g, '');

    cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
    cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
    cpf = cpf.replace(/(\d{3})(\d{1,2})$/, '$1-$2');

    event.target.value = cpf;
});

/*----------------------------- */

document.getElementById('voluntarioForm').addEventListener('submit', async(e) => {
  e.preventDefault();

  var spans = document.querySelectorAll('span');
  spans.forEach(function(span) {
      var paragrafos = span.querySelectorAll('p');
      paragrafos.forEach(function(paragrafo) {
          span.removeChild(paragrafo);
      });
  });

  var cpf = document.getElementById('idCPF').value;
  var senha = document.getElementById('idSenha').value;

  var url = "/validar/login/";

  await fetch(`${url}?cpf=${cpf}&senha=${senha}`)
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