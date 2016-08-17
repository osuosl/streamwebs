$(document).ready(function () {
    $('select').material_select();

    // Collapsible table rows
    $('.collapse-header').click(function(){
        if($(this).hasClass("collapsed")){
            $(this).nextUntil('tr.collapse-header')
                .find('td')
                .parent()
                .find('td > div')
                .slideDown("fast", function(){
                    var $set = $(this);
                    $set.replaceWith($set.contents());
                });
            $(this).removeClass("collapsed");
        } else {
            $(this).nextUntil('tr.collapse-header')
                .find('td')
                .wrapInner('<div style="display: block;" />')
                .parent()
                .find('td > div')
                .slideUp("fast");
            $(this).addClass("collapsed");
        }
    });
});
