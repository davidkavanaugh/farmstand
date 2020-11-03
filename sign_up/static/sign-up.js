$(document).ready(function () {
  const removeErrors = () => {
    $("#sign-up-errors").html("");
  };
  $("form").keyup(removeErrors);
});
