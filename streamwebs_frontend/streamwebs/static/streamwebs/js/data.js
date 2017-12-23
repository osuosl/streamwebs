$(document).ready(function () {

    $('select').material_select();

    $('.datepicker').pickadate({
        today: '',
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 15, // Creates a dropdown of 15 years to control year
        max: true, // set max to today
        format: 'yyyy-mm-dd',
    });

    $('.collapse-btn').click(function () {
        $('.collapse').toggleClass('uncollapse');
    });

    // Accidentally pressing enter will not submit the form
    $("input").bind("keypress", function(e) {
      if (e.keyCode == 13) return false;
    });

});
