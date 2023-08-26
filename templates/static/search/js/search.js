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

$(document).ready(function() {
  $('.filter_to_exclude_button').click(function() {
    var selectedValue = $(this).val();
    $('#selected_filter_to_exclude').val(selectedValue);
    $('#filter_to_exclude').submit();
  });
});
