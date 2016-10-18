$(document).ready(function () {
    $('select').material_select();

    $('.datepicker').pickadate({
        format: 'yyyy-mm-dd'
    });

    $('.collapse-btn').click(function () {
        $('.collapse').toggleClass('uncollapse');
    });
});
