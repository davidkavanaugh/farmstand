$(document).ready(function () {
  const removeErrors = () => {
    $("#edit-profile-errors").html("");
  };
  $("form").keyup(removeErrors);
});
