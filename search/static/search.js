$(document).ready(function () {
  const removeErrors = () => {
    $("#search-errors").html("");
  };
  $("form").keyup(removeErrors);
});
