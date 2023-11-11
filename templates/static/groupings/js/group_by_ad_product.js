// filtros do datatable gerenciar agrupamento
$(document).ready(function(){
    $("#produtos-table").DataTable();
  });


//Alerta com JS Fecha quando clica no botão
$(document).ready(function () {
    $(".btn-close").on("click", function () {
      $(this).closest(".alert").hide();
    });
  });


document.addEventListener("DOMContentLoaded", function() {
var alertElement = document.getElementById("myAlert");
if (alertElement) {
    setTimeout(function(){
    alertElement.remove();
    }, 5000);
}
});


document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('[id^="excluir-anuncio-"]');

    buttons.forEach(function (button) {
      button.addEventListener('click', function (event) {
        event.preventDefault();

        const groupId = button.id.replace('excluir-anuncio-', '');
        const title = button.title;

        const confirmation = confirm('Você tem certeza de que deseja excluir esse produto? Você perderá todos os dados armazenados');

        if (confirmation) {
          // Se o usuário confirmar, envie o formulário
          document.getElementById('formulario-exclusao-' + groupId).submit();
        }
      });
    });
  });
