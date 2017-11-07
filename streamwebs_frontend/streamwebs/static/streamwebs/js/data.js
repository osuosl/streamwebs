$(document).ready(function () {
    $('select').material_select();
    $('.collapse-btn').click(function () {
        $('.collapse').toggleClass('uncollapse');
    });
});
