
document.getElementById("exclude").addEventListener("click", function(event) {
    // Impedir o envio do formulário automaticamente
    event.preventDefault();
    
    // Exibir a caixa de diálogo de confirmação
    var confirmacao = confirm("Tem certeza que deseja excluir o usuário?");
    
    // Se o usuário confirmar, enviar o formulário
    if (confirmacao) {
          document.getElementById("meuFormulario").submit();
      }
});

document.getElementById("name-or-email").addEventListener("click", function(event) {
    // Impedir o envio do formulário automaticamente
    event.preventDefault();
    
    // Exibir a caixa de diálogo de confirmação
    var confirmacao = confirm("Tem certeza que quer alterar seus dados?");
    
    // Se o usuário confirmar, enviar o formulário
    if (confirmacao) {
          document.getElementById("form-name-or-email").submit();
      }
});

document.getElementById("senha").addEventListener("click", function(event) {
    // Impedir o envio do formulário automaticamente
    event.preventDefault();
    
    // Exibir a caixa de diálogo de confirmação
    var confirmacao = confirm("Tem certeza que quer alterar sua seneha?");
    
    // Se o usuário confirmar, enviar o formulário
    if (confirmacao) {
          document.getElementById("form_senha").submit();
      }
});

