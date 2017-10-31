var search_school = function search_school() {
    var input = $('input#search');
    if (input.val().length > 0) {
        $('div.search-results ul li').hide();
        var searchVal = input.val().toLowerCase();
        $('div.search-results ul li').each(function() {
            var val = $(this).find('button').text().toLowerCase();
            if (val.includes(searchVal)) {
                $(this).show();
            }
        });
        $('div.search-results').show();
    }
}

$(function() {
    var schoolOptions = $('div.school select option').toArray();
    for (var i = 0; i < schoolOptions.length; i++) {
        if (schoolOptions[i].selected === true) {
            $('p.school-selected b').text(schoolOptions[i].text);
            break;
        }
    }
    $('div.search-results button').on('click', function(e) {
        e.preventDefault();
        var schoolName = $(e.target).text();
        for (var i = 0; i < schoolOptions.length; i++) {
            if (schoolOptions[i].text === schoolName) {
                schoolOptions[i].selected = true;
                break;
            }
        }
        $('input#search').val(schoolName);
        $('p.school-selected b').text(schoolName);
        $('div.search-results').hide();
    });
    $(document).on('click', function() {
        $('div.search-results').hide();
    });
    $('input#search').on('input', function() {
        search_school();
    });
});
