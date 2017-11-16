var countSelected = function countSelected() {
    var numSelected = 0;
    $('div#canopies').find('.canopy-square.shown').each(function (i,e) {
        if($(e).hasClass('blue-grey darken-1')) {
            numSelected++;
        }
    });
    return numSelected;
}

var rewindSquares = function rewindSquares() {
    var north_shades = $('#north-form').find('input').val();
    var west_shades = $('#west-form').find('input').val();
    var east_shades = $('#east-form').find('input').val();
    var south_shades = $('#south-form').find('input').val();
    shadeSquares(north_shades, west_shades, east_shades, south_shades);
}

var shadeSquares = function shadeSquares(north_shades, west_shades, east_shades, south_shades) {
// Iterate over each of the right-most 24 bits from right to left
// If a bit is 1, shade that square
    for (var i = 0; i < 24; i++, north_shades = north_shades >>> 1) {
        if (north_shades & 1) {
            $('#canopy-north > #square-0-' + i).addClass('blue-grey darken-1');
        }
    }
    for (var i = 0; i < 24; i++, west_shades = west_shades >>> 1) {
        if (west_shades & 1) {
            $('#canopy-west #square-1-' + i).addClass('blue-grey darken-1');
        }
    }
    for (var i = 0; i < 24; i++, east_shades = east_shades >>> 1) {
        if (east_shades & 1) {
            $('#canopy-east #square-2-' + i).addClass('blue-grey darken-1');
        }
    }
    for (var i = 0; i < 24; i++, south_shades = south_shades >>> 1) {
        if (south_shades & 1) {
            $('#canopy-south #square-3-' + i).addClass('blue-grey darken-1');
        }
    }
}

$(function () {
    rewindSquares();
    var input = $("#total").find("input");
    var display = $("#percent");
    display.text("0%");

    $(".canopy-square").mousedown(function toggleSquare(evt) {
        var square = $(evt.target);
        square.toggleClass('blue-grey darken-1');

        var numSelected = countSelected();
        input.val(numSelected);
        display.text(Math.floor((numSelected) / 96 * 10000) / 100 + "%");
    });

    $('form').submit(function submit() {
        var north = 0;

        $('#canopy-north').find('.canopy-square.shown').each(function (i, e) {
            if ($(e).hasClass('blue-grey darken-1')) {
                var num = Number.parseInt(e.id.slice(9)); // Drop off the 'square-n-'
                north |= (1 << num);
            }
        });

        $('#north-form').find('input').val(north);

        var west = 0;

        $('#canopy-west').find('.canopy-square.shown').each(function (i, e) {
            if ($(e).hasClass('blue-grey darken-1')) {
                var num = Number.parseInt(e.id.slice(9)); // Drop off the 'square-n-'
                west |= (1 << num);
            }
        });

        $('#west-form').find('input').val(west);

        var east = 0;

        $('#canopy-east').find('.canopy-square.shown').each(function (i, e) {
            if ($(e).hasClass('blue-grey darken-1')) {
                var num = Number.parseInt(e.id.slice(9)); // Drop off the 'square-n-'
                east |= (1 << num);
            }
        });

        $('#east-form').find('input').val(east);

        var south = 0;

        $('#canopy-south').find('.canopy-square.shown').each(function (i, e) {
            if ($(e).hasClass('blue-grey darken-1')) {
                var num = Number.parseInt(e.id.slice(9)); // Drop off the 'square-n-'
                south |= (1 << num);
            }
        });

        var numSelected = countSelected();
        input.val(numSelected);
        $('#south-form').find('input').val(south);
    });
});
