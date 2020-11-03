$(document).ready(() => {
  const removeErrors = () => {
    $("#sign-up-errors").html("");
  };
  $("#password, #confirmPassword, #email").keyup(removeErrors);
});
