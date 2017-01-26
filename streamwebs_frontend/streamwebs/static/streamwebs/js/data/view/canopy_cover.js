$(function shadeSquares() {
    // Iterate over each of the right-most 24 bits from right to left
    // If a bit is 1, shade that square
    for (let i = 0; i < 24; i++, north_shades = north_shades >>> 1) {
        if (north_shades & 1) {
            $('#canopy-north > #square-0-' + i).addClass('blue-grey darken-1');
        }
    }

    // Iterate over each of the right-most 24 bits from right to left
    // If a bit is 1, shade that square
    for (let i = 0; i < 24; i++, west_shades = west_shades >>> 1) {
        if (west_shades & 1) {
            $('#canopy-west #square-1-' + i).addClass('blue-grey darken-1');
        }
    }

    // Iterate over each of the right-most 24 bits from right to left
    // If a bit is 1, shade that square
    for (let i = 0; i < 24; i++, east_shades = east_shades >>> 1) {
        if (east_shades & 1) {
            $('#canopy-east #square-2-' + i).addClass('blue-grey darken-1');
        }
    }

    // Iterate over each of the right-most 24 bits from right to left
    // If a bit is 1, shade that square
    for (let i = 0; i < 24; i++, south_shades = south_shades >>> 1) {
        if (south_shades & 1) {
            $('#canopy-south #square-3-' + i).addClass('blue-grey darken-1');
        }
    }
});
