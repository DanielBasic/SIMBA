//MODAL PARA CRIAR UM NOVO AGRUPAMENTO

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
if (openModalBtn !== null){
    openModalBtn.onclick = function () {
        modal.style.display = "block";
    };
}

openModalBtn.addEventListener("click", toggleModal);
closeModalBtn.addEventListener("click", toggleModal);
if (closeModalBtn !== null){
    closeModalBtn.onclick = function () {
        modal.style.display = "none";
    };
}

window.addEventListener("click", function (event) {
    if (event.target === modal) {
        toggleModal();
    }
});



// MODAL PARA EDOTAR O AGRUPAMENT
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




// // JavaScript for search filter
// document.addEventListener("DOMContentLoaded", function() {
//     const searchInput = document.getElementById("searchInput");
//     const searchButton = document.getElementById("searchButton");
//     const tableBody = document.getElementById("tableBody");
//     const rows = tableBody.getElementsByTagName("tr");

//     searchButton.addEventListener("click", performSearch);
//     searchInput.addEventListener("input", performSearch);

//     function performSearch() {
//         const searchText = searchInput.value.toLowerCase();

//         for (let i = 0; i < rows.length; i++) {
//             const row = rows[i];
//             const titleCell = row.querySelector("td:nth-child(2)"); // Assuming title is the second column
//             if (titleCell) {
//                 const title = titleCell.innerHTML.toLowerCase();
//                 const shouldDisplay = title.includes(searchText);
//                 row.style.display = shouldDisplay ? "" : "none";
//             }
//         }
//     }
// });



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



//Alerta com JS Fecha com 5 Segundo gerenciar agrupamento

document.addEventListener("DOMContentLoaded", function() {
var alertElement = document.getElementById("myAlert");
if (alertElement) {
    setTimeout(function(){
    alertElement.remove();
    }, 5000);
}
});

//Alerta com JS Fecha quando clica no botão gerenciar agrupamento
$(document).ready(function () {
    $(".btn-close").on("click", function () {
      $(this).closest(".alert").hide();
    });
  });


// filtros do datatable gerenciar agrupamento
$(document).ready(function(){
$("#my-table").DataTable();
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


document.addEventListener("DOMContentLoaded", function () {
    const tracking_infos = JSON.parse(document.getElementById('tracking_infos').textContent);
    var arrows_price = document.querySelectorAll('#arrow_price');
    var arrows_health = document.querySelectorAll('#arrow_health');
    function updateArrowsAndPercentages(arrowElements) {
        var threshold = 0;
        arrowElements.forEach(function(arrowElement) {
            var group_id = parseInt(arrowElement.getAttribute('group_id'));
            var product_id = arrowElement.getAttribute('product_id');
            var id;
            if (!isNaN(group_id)){
                id = group_id;
            }else {
                id = product_id;
            }
            console.log(id);

            var value_id_arrow = arrowElement.id;
            
            var variation_percentage ;

            if (value_id_arrow == 'arrow_price') {
                variation_percentage = 'price_variation_percentage';
            } else {
                if (value_id_arrow == 'arrow_health'){
                    variation_percentage = 'health_variation_percentage'
                }
            }

            var value_percentage = tracking_infos[id][variation_percentage];

            arrowElement.innerHTML = '';

            if (value_percentage !== 0) {
                var arrowClass = value_percentage >= threshold ? 'green' : 'red';

                var arrowIcon = document.createElement('i');
                arrowIcon.className = 'fas fa-sort-up';
                arrowElement.style.backgroundColor = arrowClass;
                arrowElement.appendChild(arrowIcon);
            }

            var percentageCircle = document.createElement('div');
            percentageCircle.className = 'percentage-circle';
            percentageCircle.innerText = value_percentage + '%';

            // Append the percentage circle to the container
            arrowElement.appendChild(percentageCircle);
        });
    }
    updateArrowsAndPercentages(arrows_price);
    updateArrowsAndPercentages(arrows_health);
});
