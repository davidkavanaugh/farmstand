$(document).ready(function () {
  const removeErrors = () => {
    $("#search-errors").html("");
  };
  $("form").keyup(removeErrors);
  $('#search-btn').click(function(){
    $('form').attr('action', $('#zipCode').val());
  });
});

