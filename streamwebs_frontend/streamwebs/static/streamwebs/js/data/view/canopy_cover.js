$(function shadeSquares() {
    let shades = {{ canopy_cover.north_cc }};

    // Iterate over each of the right-most 24 bits from right to left
    // If a bit is 1, shade that square
    for (let i = 0; i < 24; i++, shades = shades >>> 1) {
        if (shades & 1) {
            $('#canopy-north > #square-' + i).addClass('shaded');
        }
    }

    shades = {{ canopy_cover.west_cc }};

    // Iterate over each of the right-most 24 bits from right to left
    // If a bit is 1, shade that square
    for (let i = 0; i < 24; i++, shades = shades >>> 1) {
        if (shades & 1) {
            $('#canopy-west #square-' + i).addClass('shaded');
        }
    }

    shades = {{ canopy_cover.east_cc }};

    // Iterate over each of the right-most 24 bits from right to left
    // If a bit is 1, shade that square
    for (let i = 0; i < 24; i++, shades = shades >>> 1) {
        if (shades & 1) {
            $('#canopy-east #square-' + i).addClass('shaded');
        }
    }

    shades = {{ canopy_cover.south_cc }};

    // Iterate over each of the right-most 24 bits from right to left
    // If a bit is 1, shade that square
    for (let i = 0; i < 24; i++, shades = shades >>> 1) {
        if (shades & 1) {
            $('#canopy-south #square-' + i).addClass('shaded');
        }
    }
});
