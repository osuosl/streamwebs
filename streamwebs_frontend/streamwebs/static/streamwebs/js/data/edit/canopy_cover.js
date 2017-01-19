$(function () {
    $("#total input").attr('readonly', 'true');
    $("#total input").attr('num', 0);

    $(".canopy-square.hidden").mousedown(function(evt) {
      evt.preventDefault();
    });

    $(".canopy-square").mousedown(function toggleSquare(evt) {
        const square = $(evt.target);

        square.toggleClass('shaded');

        if (square.hasClass('shaded')) {
            let oldval = Number.parseInt($("#total input").attr('num'));
            $("#total input").attr('num', oldval+1);
            $("#total input").val(Math.floor((oldval+1) / 96 * 10000) / 100);
        } else {
            let oldval = Number.parseInt($("#total input").attr('num'));
            $("#total input").attr('num', oldval-1);
            $("#total input").val(Math.floor((oldval-1) / 96 * 10000) / 100);
        }

        evt.preventDefault();
    });

    $('#submit').click(function sendData() {
        let north = 0;

        $('#canopy-north .canopy-square.shown').each((i, e) => {
            if ($(e).hasClass('shaded')) {
                let num = Number.parseInt(e.id.slice(7)); // Drop off the 'square-'

                north |= (1 << num);
            }
        });

        $('#north-form input').val(north);

        let west = 0;

        $('#canopy-west .canopy-square.shown').each((i, e) => {
            if ($(e).hasClass('shaded')) {
                let num = Number.parseInt(e.id.slice(7)); // Drop off the 'square-'

                west |= (1 << num);
            }
        });

        $('#west-form input').val(west);

        let east = 0;

        $('#canopy-east .canopy-square.shown').each((i, e) => {
            if ($(e).hasClass('shaded')) {
                let num = Number.parseInt(e.id.slice(7)); // Drop off the 'square-'

                east |= (1 << num);
            }
        });

        $('#east-form input').val(east);

        let south = 0;

        $('#canopy-south .canopy-square.shown').each((i, e) => {
            if ($(e).hasClass('shaded')) {
                let num = Number.parseInt(e.id.slice(7)); // Drop off the 'square-'

                south |= (1 << num);
            }
        });

        $('#south-form input').val(south);
    });
});
