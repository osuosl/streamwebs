$(function () {
    const input = $("#total").find("input");
    input.attr('readonly', 'true');
    input.attr('num', 0);

    $(".canopy-square.hidden").mousedown(function(evt) {
      evt.preventDefault();
    });

    $(".canopy-square").mousedown(function toggleSquare(evt) {
        const square = $(evt.target);

        square.toggleClass('shaded');

        if (square.hasClass('shaded')) {
            let oldval = Number.parseInt(input.attr('num'));
            input.attr('num', oldval+1);
            input.val(Math.floor((oldval+1) / 96 * 10000) / 100);
        } else {
            let oldval = Number.parseInt(input.attr('num'));
            input.attr('num', oldval-1);
            input.val(Math.floor((oldval-1) / 96 * 10000) / 100);
        }

        evt.preventDefault();
    });

    $('form').submit(function submit() {
        input.val(input.attr('num'));

        let north = 0;

        $('#canopy-north').find('.canopy-square.shown').each((i, e) => {
            if ($(e).hasClass('shaded')) {
                let num = Number.parseInt(e.id.slice(9)); // Drop off the 'square-n-'

                north |= (1 << num);
            }
        });

        $('#north-form').find('input').val(north);

        let west = 0;

        $('#canopy-west').find('.canopy-square.shown').each((i, e) => {
            if ($(e).hasClass('shaded')) {
                let num = Number.parseInt(e.id.slice(9)); // Drop off the 'square-n-'

                west |= (1 << num);
            }
        });

        $('#west-form').find('input').val(west);

        let east = 0;

        $('#canopy-east').find('.canopy-square.shown').each((i, e) => {
            if ($(e).hasClass('shaded')) {
                let num = Number.parseInt(e.id.slice(9)); // Drop off the 'square-n-'

                east |= (1 << num);
            }
        });

        $('#east-form').find('input').val(east);

        let south = 0;

        $('#canopy-south').find('.canopy-square.shown').each((i, e) => {
            if ($(e).hasClass('shaded')) {
                let num = Number.parseInt(e.id.slice(9)); // Drop off the 'square-n-'

                south |= (1 << num);
            }
        });

        $('#south-form').find('input').val(south);
    });
});
