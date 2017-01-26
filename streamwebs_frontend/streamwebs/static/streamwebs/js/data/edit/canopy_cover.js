$(function () {
    const input = $("#total").find("input");
    const display = $("#percent");

    $(".canopy-square").mousedown(function toggleSquare(evt) {
        const square = $(evt.target);

        square.toggleClass('blue-grey darken-1');

        if (square.hasClass('blue-grey darken-1')) {
            let oldval = Number.parseInt(input.val());
            input.val(oldval+1);
            display.text(Math.floor((oldval+1) / 96 * 10000) / 100 + "%");
        } else {
            let oldval = Number.parseInt(input.val());
            input.val(oldval-1);
            display.text(Math.floor((oldval-1) / 96 * 10000) / 100 + "%");
        }
    });

    $('form').submit(function submit() {
        let north = 0;

        $('#canopy-north').find('.canopy-square.shown').each((i, e) => {
            if ($(e).hasClass('blue-grey darken-1')) {
                let num = Number.parseInt(e.id.slice(9)); // Drop off the 'square-n-'

                north |= (1 << num);
            }
        });

        $('#north-form').find('input').val(north);

        let west = 0;

        $('#canopy-west').find('.canopy-square.shown').each((i, e) => {
            if ($(e).hasClass('blue-grey darken-1')) {
                let num = Number.parseInt(e.id.slice(9)); // Drop off the 'square-n-'

                west |= (1 << num);
            }
        });

        $('#west-form').find('input').val(west);

        let east = 0;

        $('#canopy-east').find('.canopy-square.shown').each((i, e) => {
            if ($(e).hasClass('blue-grey darken-1')) {
                let num = Number.parseInt(e.id.slice(9)); // Drop off the 'square-n-'

                east |= (1 << num);
            }
        });

        $('#east-form').find('input').val(east);

        let south = 0;

        $('#canopy-south').find('.canopy-square.shown').each((i, e) => {
            if ($(e).hasClass('blue-grey darken-1')) {
                let num = Number.parseInt(e.id.slice(9)); // Drop off the 'square-n-'

                south |= (1 << num);
            }
        });

        $('#south-form').find('input').val(south);
    });
});
