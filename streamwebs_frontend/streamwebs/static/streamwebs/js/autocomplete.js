
/**************************
* Auto complete plugin  *
* Direct copy from MaterializeCSS AutoComplete plugin. *
* Contains modifications to remove image support *
*************************/
$.fn.autocomplete_noimg = function (options) {
    // Defaults
    var defaults = {
        data: {}
    };

    options = $.extend(defaults, options);

    return this.each(function() {
        var $input = $(this);
        var data = options.data,
            $inputDiv = $input.closest('.input-field'); // Div to append on

        var onSelect = options.onSelect;

        // Check if data isn't empty
        if (!$.isEmptyObject(data)) {
        // Create autocomplete element
        var $autocomplete = $('<ul class="autocomplete-content dropdown-content"></ul>');

        // Append autocomplete element
        if ($inputDiv.length) {
            $inputDiv.append($autocomplete); // Set ul in body
        } else {
            $input.after($autocomplete);
        }

        var highlight = function(string, $el) {
            var matchStart = $el.text().toLowerCase().indexOf("" + string.toLowerCase() + ""),
                matchEnd = matchStart + string.length - 1,
                beforeMatch = $el.text().slice(0, matchStart),
                matchText = $el.text().slice(matchStart, matchEnd + 1),
                afterMatch = $el.text().slice(matchEnd + 1);
            $el.html("<span class='black-text'>" + beforeMatch + "<span class='teal-text text-lighten-2'>" + matchText + "</span>" + afterMatch + "</span>");
        };

        // Perform search
        $input.on('keyup', function (e) {
            // Capture Enter
            if (e.which === 13) {
            $autocomplete.find('li').first().click();
            return;
            }

            var val = $input.val().toLowerCase();
            $autocomplete.empty();

            // Check if the input isn't empty
            if (val !== '') {
                for(var key in data) {
                    if (data.hasOwnProperty(key) &&
                        key.toLowerCase().includes(val))
                    {
                        var autocompleteOption = $('<li value='+data[key]+'></li>');
                        autocompleteOption.append('<span>'+ key +'</span>');
                        $autocomplete.append(autocompleteOption);

                        highlight(val, autocompleteOption);
                    }
                }
            }
        });

        // Set input value
        $autocomplete.on('click', 'li', function () {
            var label = $(this).text().trim();
            var value = $(this).attr('value');
            //$input.val(label);
            $autocomplete.empty();
            onSelect(label, value);
        });
        }
    });
};
