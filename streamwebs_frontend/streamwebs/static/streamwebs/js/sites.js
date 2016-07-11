var dropdownShown = 0;
function search() {
    console.log('Searched!');

    var search_value = $('#search').val().toLowerCase();
    var stewards = $('#steward_box').prop('checked');
    var salmon = $('#salmon_box').prop('checked');
    var available = $('#available_box').prop('checked');
    var none = !stewards && !salmon && !available;
    dropdownShown = 0;

    $('.search-item').each(function () {
        var name = $(this).text().toLowerCase();
        var search_point = $('#search').offset().top + parseInt($('#search').css('height'));

        if ((none ||
            (stewards && $(this).hasClass('steward')) ||
            (salmon && $(this).hasClass('salmon')) ||
            (available && $(this).hasClass('available'))) &&
        search_value && name.includes(search_value)) {
            $(this).removeClass('hide');
            $(this).css("top", search_point + (dropdownShown * 40));
            $(this).css("left", $('#search').offset().left);
            dropdownShown += 1;
        } else {
            $(this).addClass('hide');
        }
    });
}

function goto(slug) {
    window.location.href = "/streamwebs/site/" + slug;
}

function submit_map(site) {
    goto(site);
}

var map;

var path = "m 0,0 c -7.08163,-14.59707 -5.50487,-20.97294 5.18667,-20.97294 " +
           "10.69154,0 12.2683,6.37587 5.18667,20.97294 -2.4156,4.97919 " +
           "-4.74961,9.05306 -5.18667,9.05306 -0.43706,0 -2.77107,-4.07387 " +
           "-5.18667,-9.05306 z";
var markers = {
    steward: {
        path: path,
        fillColor: "#0000FF",
        fillOpacity: 1,
        strokeColor: "#000000",
        strokeWeight: 2,
    },
    salmon: {
        path: path,
        fillColor: "#FF7F00",
        fillOpacity: 1,
        strokeColor: "#000000",
        strokeWeight: 2,
    },
    available: {
        path: path,
        fillColor: "#FF0000",
        fillOpacity: 1,
        strokeColor: "#000000",
        strokeWeight: 2,
    },
}

function initialize() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 7,
        center: new google.maps.LatLng(44, -122),
        mapTypeId: google.maps.MapTypeId.ROADMAP,
    });

    var latSum = 0, lngSum = 0;

    for (let site of sites) {
        site.marker = new google.maps.Marker({
            map: map,
            position: new google.maps.LatLng(site.lat, site.lng),
            title: site.name,
            icon: markers[site.type],
        });
        site.infoWindow = new google.maps.InfoWindow({
            content: '<p><a href="javascript:submit_map(\'' + site.slug + '\')">' + site.name + '</a></p><p>' + site.description + '</p>',
        });
        site.marker.addListener('click', function () {
            for (let otherSite of sites) {
                otherSite.infoWindow.close();
            }
            site.infoWindow.open(map, site.marker);
        });

        latSum += site.lat;
        lngSum += site.lng;
    }

    map.setCenter(new google.maps.LatLng(latSum / sites.length,
                                         lngSum / sites.length));
}

$(document).ready(function () {
    initialize();
});
