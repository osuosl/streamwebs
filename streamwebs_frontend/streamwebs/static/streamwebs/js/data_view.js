$(document).ready(function () {
    $('select').material_select();

    function collapse(obj) {
        if($(obj).hasClass("collapsed")) {
            $(obj).nextUntil('tr.collapse-header')
                .find('td')
                .parent()
                .find('td > div')
                .slideDown("fast", function () {
                    var $set = $(this);
                    $set.replaceWith($set.contents());
                });
            $(obj).removeClass("collapsed");
        } else {
            $(obj).nextUntil('tr.collapse-header')
                .find('td')
                .wrapInner('<div style="display: block;" />')
                .parent()
                .find('td > div')
                .slideUp("fast");
            $(obj).addClass("collapsed");
        }
    }

    collapse($('.collapse-header'));

    // Collapsible table rows
    $('.collapse-header').click(function () {
        collapse(this);
    });
});
