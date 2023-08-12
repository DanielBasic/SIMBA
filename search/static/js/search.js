
$(document).ready(function() {
    $('.filter_to_exclude_button').click(function() {
      var selectedValue = $(this).val();
      $('#selected_filter_to_exclude').val(selectedValue);
      $('#filter_to_exclude').submit();
    });
  });