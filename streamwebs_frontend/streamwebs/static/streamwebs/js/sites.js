var dropdownShown = 0;
function search() {
    console.log('Searched!');

    var search_value = $('#search').val().toLowerCase();

    dropdownShown = 0;

    $('.search-item').each(function () {
        var name = $(this).text().toLowerCase();
        var search_point = $('#search').offset().top + parseInt($('#search').css('height'));

        if (search_value && name.includes(search_value)) {
            $(this).removeClass('hide');
            $(this).css("top", search_point + (dropdownShown * 40));
            $(this).css("left", $('#search').offset().left);
            dropdownShown += 1;
        } else {
            $(this).addClass('hide');
        }
    });
}

var map;

var path = "m 0,0 c -7.08163,-14.59707 -5.50487,-20.97294 5.18667,-20.97294 " +
           "10.69154,0 12.2683,6.37587 5.18667,20.97294 -2.4156,4.97919 " +
           "-4.74961,9.05306 -5.18667,9.05306 -0.43706,0 -2.77107,-4.07387 " +
           "-5.18667,-9.05306 z";

function initialize() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 7,
        center: new google.maps.LatLng(44, -122),
        mapTypeId: window.mapTypeId,
    });

    var latSum = 0, lngSum = 0;

    var markerList = [];
    var infoWindows = [];

    for (var i = 0; i < sites.length; i++) {
        var site = sites[i];

        markerList[i] = new google.maps.Marker({
            map: map,
            position: new google.maps.LatLng(site.lat, site.lng),
            title: site.name,
            icon: {
              path: path,
              fillColor: "#FF0000",
              fillOpacity: 1,
              strokeColor: "#000000",
              strokeWeight: 2,
            },
        });

        markerList[i].index = i;

        infoWindows[i] = new google.maps.InfoWindow({
            content: '<p><a href="' + site.slug + '">' + site.name + '</a></><p>' + site.description + '</p>',
        });

        markerList[i].addListener('click', function () {
            for (var otherWindow of infoWindows) {
                otherWindow.close();
            }

            infoWindows[this.index].open(map, markerList[this.index]);
        });

        lngSum += site.lng;
        latSum += site.lat;
    }

    // map.setCenter(new google.maps.LatLng(lngSum / sites.length,
    //                                      latSum / sites.length));
}

$(document).ready(function () {
    initialize();
});
