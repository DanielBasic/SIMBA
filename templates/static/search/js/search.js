document.addEventListener("DOMContentLoaded", function() {
  var selectAllCheckbox = document.getElementById("select-all-products");
  var checkboxes = document.querySelectorAll(".checkbox_product");
  var myButton = document.getElementById("set_products");
  var isButtonVisible = false; 

  selectAllCheckbox.addEventListener("change", function() {
    checkboxes.forEach(function(checkbox) {
      checkbox.checked = selectAllCheckbox.checked;
    });

    var anyChecked = document.querySelector(".checkbox_product:checked");
    if (anyChecked) {
      myButton.style.display = "block";
    } else {
      myButton.style.display = "none";
    }
  });

  checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener("change", function() {
      var anyChecked = document.querySelector(".checkbox_product:checked");
      if (anyChecked) {
        myButton.style.display = "block";
      } else {
        myButton.style.display = "none";
      }

      var allChecked = true;
      checkboxes.forEach(function(item) {
        if (!item.checked) {
          allChecked = false;
        }
      });
      selectAllCheckbox.checked = allChecked;
    });
  });

  window.addEventListener("scroll", function() {
    if (isButtonVisible) {
      if (window.scrollY > 200) {
        myButton.style.display = "block";
      } else {
        myButton.style.display = "none";
      }
    }
  });
});


// JS para excluir filtrs 
$(document).ready(function() {
  $('.filter_to_exclude_button').click(function() {
    var selectedValue = $(this).val();
    $('#selected_filter_to_exclude').val(selectedValue);
    $('#filter_to_exclude').submit();
  });
});

function removeRequiredAttribute(elementId) {
  const element = document.getElementById(elementId);
  if (element) {
    element.removeAttribute('required');
  }
}


function addRequiredAttribute(elementId) {
  const element = document.getElementById(elementId);
  if (element) {
    element.setAttribute('required', 'required');
  }
}


document.addEventListener("DOMContentLoaded", function() {
  const modal = document.getElementById("addProductsToGroup_modal");
  const openBtn = document.getElementById("set_products");
  var set_products_button = document.getElementById("set_products");
  const openCreationGroup = document.getElementById('openCreationGroup');
  const groupByAd_content = document.getElementById('userGroupByAd');
  const creationGroup_content = document.getElementById('createNewGroup');
  const goBackToGroups = document.getElementById('goBackToGroups');
  var imageInput = "image_field";
  var titleInput = 'title_field';
  const addProductsIntoGroup = document.getElementById('addProductsIntoGroup');
  const groupByAd = document.getElementById("groupByAd")

  openBtn.addEventListener("click", function() {
    modal.style.display = "block";
    console.log(listOfGroupByAd);
    set_products_button.style.display = "none";
    

    if (listOfGroupByAd !== 'None') {
      creationGroup_content.style.display = 'none';
      groupByAd_content.style.display = 'block';
      openCreationGroup.style.display = 'block';
      creationGroup_content.style.display = 'none';
      goBackToGroups.style.display = 'none';
      removeRequiredAttribute("image_field");
      removeRequiredAttribute("title_field");
      addRequiredAttribute("groupByAd");
      addProductsIntoGroup.action = addProductsIntoGroup.getAttribute('add_products_into_GroupByAd')
    } else {
        creationGroup_content.style.display = 'block';
        groupByAd_content.style.display = 'none';
        openCreationGroup.style.display = 'none';
        creationGroup_content.style.display = 'block';
        goBackToGroups.style.display = 'none';
        addProductsIntoGroup.action = addProductsIntoGroup.getAttribute('create_new_GroupByAd_addProductsInIt')
        addRequiredAttribute("image_field");
        addRequiredAttribute("title_field");
        removeRequiredAttribute("groupByAd");
    }
  });
  
  modal.querySelector(".close").addEventListener("click", function() {
    modal.style.display = "none";
    set_products_button.style.display = "block";
  });
  
  openCreationGroup.addEventListener('click', function() {
    groupByAd_content.style.display = 'none';
    creationGroup_content.style.display = 'block';
    goBackToGroups.style.display = 'block';
    openCreationGroup.style.display = 'none';
    addRequiredAttribute("image_field");
    addRequiredAttribute("title_field");
    removeRequiredAttribute("groupByAd");
    addProductsIntoGroup.action = addProductsIntoGroup.getAttribute('create_new_GroupByAd_addProductsInIt')
  });

  goBackToGroups.addEventListener('click', function(){
    groupByAd_content.style.display = 'block';
    creationGroup_content.style.display = 'none';
    goBackToGroups.style.display = 'none';
    openCreationGroup.style.display = 'block';
    removeRequiredAttribute("image_field");
    removeRequiredAttribute("title_field");
    addRequiredAttribute("groupByAd");
    addProductsIntoGroup.action = addProductsIntoGroup.getAttribute('add_products_into_GroupByAd')
  });
});


// JS para a mudança de pagina
document.querySelectorAll(".pagination-link").forEach(function(link) {
  link.addEventListener("click", function(event) {
    event.preventDefault();
    
    var currentURL = window.location.href;
    var newHref = this.getAttribute("href");
    
    if (currentURL.indexOf("?") !== -1) {
        window.location.href = currentURL + "&" + newHref;
    } else {
        window.location.href = currentURL + "?" + newHref;
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const radioContainers = document.querySelectorAll(".radio-container");

  radioContainers.forEach(function (container) {
    container.addEventListener("click", function () {
      const radio = container.querySelector('input[type="radio"]');
      if (radio) {
        radio.checked = true;
      }
    });
  });
});