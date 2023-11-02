// modal para adicionar no agrupamento

const modal = document.getElementById("myModal");
const openModalBtn = document.getElementById("openModal");
const closeModalBtn = document.getElementById("closeModal");

let modalIsOpen = false;

function toggleModal() {
    if (modalIsOpen) {
        modal.style.display = "none"; // Fecha o modal
    } else {
        modal.style.display = "block"; // Abre o modal
    }
    modalIsOpen = !modalIsOpen; // Inverte o estado do modal
}

openModalBtn.addEventListener("click", toggleModal);
closeModalBtn.addEventListener("click", toggleModal);

window.addEventListener("click", function (event) {
    if (event.target === modal) {
        toggleModal();
    }
});




// modal para editar o agrupamento
// const modall = document.getElementById("myModall");
// const openModallBtn = document.getElementById("openModall");
// const closeModallBtn = document.getElementById("closeModall");
// const titleToModify = document.getElementById("title-modify");
// const imageToModify = document.getElementById("image-modify");
// const groupIdToModify = document.getElementById("group-id-modify");
// var title = openModallBtn.getAttribute("title")
// var group_id = openModallBtn.getAttribute("group_id")

// let modallIsOpen = false;

// function toggleModall() {
//     if (modallIsOpen) {
//         modall.style.display = "none"; // Fecha o modal
//         imageToModify.value = "";
//         titleToModify.value = "";
//         groupIdToModify.value = "";

//     } else {
//         modall.style.display = "block"; // Abre o modal
//         titleToModify.value = title;
//         groupIdToModify.value = parseInt(group_id) ;
        
//     }
//     modallIsOpen = !modallIsOpen; // Inverte o estado do modal

// }

// openModallBtn.addEventListener("click", toggleModall);
// closeModallBtn.addEventListener("click", toggleModall);


const openModallBtns = document.querySelectorAll(".edit-button");
const closeModallBtn = document.getElementById("closeModall");
const modall = document.getElementById("myModall");
const titleToModify = document.getElementById("title-modify");
const imageToModify = document.getElementById("image-modify");
const groupIdToModify = document.getElementById("group-id-modify");

openModallBtns.forEach((openModallBtn) => {
    openModallBtn.addEventListener("click", () => {
        const group_id = openModallBtn.getAttribute("group_id");
        const title = openModallBtn.getAttribute("title");
        const image = openModallBtn.getAttribute("image");

        titleToModify.value = title;
        imageToModify.value = "";
        groupIdToModify.value = parseInt(group_id);

        modall.style.display = "block";
    });
});

closeModallBtn.addEventListener("click", () => {
    modall.style.display = "none";

    titleToModify.value = "";
    imageToModify.value = "";
    groupIdToModify.value = "";
});









// JavaScript for search filter
document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("searchInput");
    const searchButton = document.getElementById("searchButton");
    const tableBody = document.getElementById("tableBody");
    const rows = tableBody.getElementsByTagName("tr");

    searchButton.addEventListener("click", performSearch);
    searchInput.addEventListener("input", performSearch);

    function performSearch() {
        const searchText = searchInput.value.toLowerCase();

        for (let i = 0; i < rows.length; i++) {
            const row = rows[i];
            const titleCell = row.querySelector("td:nth-child(2)"); // Assuming title is the second column
            if (titleCell) {
                const title = titleCell.innerHTML.toLowerCase();
                const shouldDisplay = title.includes(searchText);
                row.style.display = shouldDisplay ? "" : "none";
            }
        }
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const clickableDivs = document.querySelectorAll(".group-details");

    clickableDivs.forEach(function (div) {
        div.addEventListener("click", function () {
            const clickedDivId = div.getAttribute("group_id");

            // Create a new form element
            const form = document.createElement("form");
            form.method = "get";
            form.action = "/groupings/group";

            const hiddenInput = document.createElement("input");
            hiddenInput.type = "hidden";
            hiddenInput.name = "group_id";
            hiddenInput.value = parseInt(clickedDivId);

            form.appendChild(hiddenInput);

            document.body.appendChild(form);
            form.submit();
        });
    });
});



//Alerta com JS Fecha com 5 Segundo

document.addEventListener("DOMContentLoaded", function() {
var alertElement = document.getElementById("myAlert");
if (alertElement) {
    setTimeout(function(){
    alertElement.remove();
    }, 5000);
}
});

//Alerta com JS Fecha quando clica no botão
$(document).ready(function () {
    $(".btn-close").on("click", function () {
      $(this).closest(".alert").hide();
    });
  });


// filtros do datatable
$(document).ready(function(){
$("#my-table").DataTable();
});

// filtros do datatable
$(document).ready(function(){
$("#produtos-table").DataTable();
});



// confirmar se o usuario realemten vai excluir o agrupamento
document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('[id^="excluir-anuncio-"]');

    buttons.forEach(function (button) {
      button.addEventListener('click', function (event) {
        event.preventDefault();

        const groupId = button.id.replace('excluir-anuncio-', '');
        const title = button.title;

        const confirmation = confirm('Você tem certeza de que deseja excluir o grupo "' + title + '"?   Você perdera todos os produtos que estão dentro desse agrupamento');

        if (confirmation) {
          // Se o usuário confirmar, envie o formulário
          document.getElementById('formulario-exclusao-' + groupId).submit();
        }
      });
    });
  });
