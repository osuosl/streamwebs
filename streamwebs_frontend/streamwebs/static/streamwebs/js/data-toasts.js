$(document).ready(function() {
  $('ul.errorlist').hide();
  if (ERROR_TOAST) Materialize.toast(ERROR_TOAST, 10000, 'red', 'center');
});
