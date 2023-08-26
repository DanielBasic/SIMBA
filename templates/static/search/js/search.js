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


document.addEventListener("DOMContentLoaded", function() {
  var showMoreButtons = document.querySelectorAll(".show-more-filters");

  showMoreButtons.forEach(function(button) {
    button.addEventListener("click", function() {
      var categoryHeading = button.previousElementSibling; // Get the h2 element
      var radioInputs = categoryHeading.nextElementSibling.querySelectorAll(".hidden-radio");
      var labels = categoryHeading.nextElementSibling.querySelectorAll(".hidden-label");

      for (var i = 0; i < radioInputs.length; i++) {
        if (i < 5) {
          radioInputs[i].style.display = "block";
          labels[i].style.display = "block";
        } else {
          radioInputs[i].style.display = "none";
          labels[i].style.display = "none";
        }
      }

      button.style.display = "none"; // Hide the "Show More" button
    });
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