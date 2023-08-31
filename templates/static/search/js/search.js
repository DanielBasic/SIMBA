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

document.addEventListener("DOMContentLoaded", function() {
  const modal = document.getElementById("addProductsToGroup_modal");
  const openBtn = document.getElementById("set_products");
  var set_products_button = document.getElementById("set_products");
  const openCreationGroup = document.getElementById('openCreationGroup');
  const groupByAd_content = document.getElementById('userGroupByAd');
  const creationGroup_content = document.getElementById('createNewGroup');
  const goBackToGroups = document.getElementById('goBackToGroups');

  openBtn.addEventListener("click", function() {
    modal.style.display = "block";
    creationGroup_content.style.display = 'none';
    set_products_button.style.display = "none";
    groupByAd_content.style.display = 'block';
    openCreationGroup.style.display = 'block';
    creationGroup_content.style.display = 'none';
    goBackToGroups.style.display = 'none';
    
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
  });

  goBackToGroups.addEventListener('click', function(){
    groupByAd_content.style.display = 'block';
    creationGroup_content.style.display = 'none';
    goBackToGroups.style.display = 'none';
    openCreationGroup.style.display = 'block';
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