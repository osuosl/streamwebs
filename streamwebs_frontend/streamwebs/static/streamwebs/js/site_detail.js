var map;

var path = "m 0,0 c -7.08163,-14.59707 -5.50487,-20.97294 5.18667,-20.97294 " +
           "10.69154,0 12.2683,6.37587 5.18667,20.97294 -2.4156,4.97919 " +
           "-4.74961,9.05306 -5.18667,9.05306 -0.43706,0 -2.77107,-4.07387 " +
           "-5.18667,-9.05306 z";

var initialize = function initialize() {
    map = new google.maps.Map(document.getElementById("detail_map"), {
        zoom: 15,
        maxZoom: 20,
        minZoom: 1,
        center: new google.maps.LatLng(site_location.y, site_location.x),
        mapTypeId: window.mapTypeId,
        disableDefaultUI: true,
        draggable: true,
        clickableIcons: false
    });

    new google.maps.Marker({
        map: map,
        position: new google.maps.LatLng(site_location.y, site_location.x),
        title: site_name,
        icon: {
          path: path,
          fillColor: "#FF0000",
          fillOpacity: 1,
          strokeColor: "#000000",
          strokeWeight: 2
        }
    });

    updateDimension();
    $(window).on('hashchange',listUpdate);
    listUpdate();
}

var updateDimension= function updateDimension() {

    if ($(document).width() > 993) {
        var ratio = boxRatio;
    } else {
        var ratio = boxRatioNarrow;
    }
    var height = $('div.resp_box').width() * ratio;
    $('div.resp_box').height(height);
    centerImage(ratio);
}

var centerImage = function centerImage(ratio) {
    if (imgRatio > ratio) {
        $('img#site_detail_image').width('100%');
        var marginTop = ($('div.resp_box').height()
          - $('img#site_detail_image').height())/2;
        $('img#site_detail_image').css('margin-top', marginTop + 'px');
    } else {
        $('img#site_detail_image').height('100%');
        var marginLeft = ($('div.resp_box').width()
          - $('img#site_detail_image').width())/2;
        $('img#site_detail_image').css('margin-left', marginLeft + 'px');
    }
}

var listUpdate = function listUpdate() {
    var list = $('#data-sheet-list');
    var page = parseInt(window.location.hash.slice(1),10) || 1;
    var page_data = JSON.parse(JSON.stringify(sheet_data.slice((page-1)*10, page*10)));

    list.html('');
    for (var datum of page_data) {
        var listItem = $('<li></li>').addClass('collection-item');
        if (datum.type == 'school') {
            var schoolName = $('<p></p>').attr('href', '#').text(datum.name);
            listItem.append(schoolName);
        }
        else {
            var itemLink = $('<a></a>').attr('href', '/sites/'+site_slug+'/'+datum.uri+'/'+datum.id);
            itemLink.text(datum.type+' data: '+datum.date);
            listItem.append(itemLink);
        }

        list.append(listItem);
    }

    if (page === 1) {
        $('#first-page').removeClass('wave-effects').addClass('disabled');
    } else {
        $('#first-page').addClass('wave-effects').removeClass('disabled');
    }

    if (page === page_count) {
        $('#last-page').removeClass('wave-effects').addClass('disabled');
    } else {
        $('#last-page').addClass('wave-effects').removeClass('disabled');
    }

    $('.page-select').removeClass('active').addClass('wave-effects');
    $('#page-'+page).addClass('active').removeClass('wave-effects');
}

$(document).ready(function () {

});
