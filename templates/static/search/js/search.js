document.addEventListener("DOMContentLoaded", function() {
  var selectAllCheckbox = document.getElementById("select-all-products");
  var checkboxes = document.querySelectorAll(".checkbox_product");

  selectAllCheckbox.addEventListener("change", function() {
    checkboxes.forEach(function(checkbox) {
      checkbox.checked = selectAllCheckbox.checked;
    });
  });

  checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener("change", function() {
      if (!checkbox.checked) {
        selectAllCheckbox.checked = false;
      } else {
        var allChecked = true;
        checkboxes.forEach(function(item) {
          if (!item.checked) {
            allChecked = false;
          }
        });
        selectAllCheckbox.checked = allChecked;
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", function() {
  var checkboxes = document.querySelectorAll(".checkbox_product");
  var myButton = document.getElementById("set_products");

  checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener("change", function() {
      var anyChecked = false;
      checkboxes.forEach(function(item) {
        if (item.checked) {
          anyChecked = true;
        }
      });

      if (anyChecked) {
        myButton.style.display = "block";
      } else {
        myButton.style.display = "none";
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", function() {
  var floatingButton = document.getElementById("floating-button");

  window.addEventListener("scroll", function() {
    if (window.scrollY > 200) {  // Adjust the scroll threshold as needed
      floatingButton.style.display = "block";
    } else {
      floatingButton.style.display = "none";
    }
  });
});


$(document).ready(function() {
    $('.filter_to_exclude_button').click(function() {
      var selectedValue = $(this).val();
      $('#selected_filter_to_exclude').val(selectedValue);
      $('#filter_to_exclude').submit();
      
    });
  });

