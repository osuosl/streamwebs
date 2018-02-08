
function initialize() {
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
}

function updateDimension() {
    if ($(document).width() > 993) {
        var ratio = boxRatio;
    } else {
        var ratio = boxRatioNarrow;
    }
    var height = $('div.resp_box').width() * ratio;
    $('div.resp_box').height(height);
    centerImage(ratio);
}

function centerImage(ratio) {
    if (imgRatio > ratio) {
        $('img#site_detail_image').width('100%');
        var marginTop = ($('div.resp_box').height()
            - $('img#site_detail_image').height()) / 2;
        $('img#site_detail_image').css('margin-top', marginTop + 'px');
    } else {
        $('img#site_detail_image').height('100%');
        var marginLeft = ($('div.resp_box').width()
            - $('img#site_detail_image').width()) / 2;
        $('img#site_detail_image').css('margin-left', marginLeft + 'px');
    }
}


function filter_datasheets(page) {
    if (datasheet_page != page) {
        datasheet_page = page;
        update_url_params();
    }

    var list = $('#datasheets');
    var new_page = (page-1)*num_elements_page;
    var page_data = JSON.parse(JSON.stringify(sheet_data.slice(new_page, new_page+num_elements_page)));

    list.html('');
    for (var datum of page_data) {
        if (datum.type == 'school') {
            var listItem = $('<li></li>').addClass('collection-item');
            var schoolName = $('<p></p>').attr('href', '#').text(datum.name);
            listItem.append(schoolName);
        }
        else {
            var listItem = $('<a></a>').addClass('collection-item');
            listItem.attr('href', '/sites/'+site_slug+'/'+datum.uri+'/'+datum.id);
            listItem.text(datum.type + ' data: ' + datum.date);
        }

        list.append(listItem);
    }

    if (page == 1) {
        $('#first-page-datasheet').removeClass('wave-effects').addClass('disabled');
    } else {
        $('#first-page-datasheet').addClass('wave-effects').removeClass('disabled');
    }

    if (page == page_count_ds) {
        $('#last-page-datasheet').removeClass('wave-effects').addClass('disabled');
    } else {
        $('#last-page-datasheet').addClass('wave-effects').removeClass('disabled');
    }

    $('.page-select-datasheet').removeClass('active').addClass('wave-effects');
    $('#page-'+page+'-datasheet').addClass('active').removeClass('wave-effects');
}

function filter_gallery(page) {
    if (gallery_page != page) {
        gallery_page = page;
        update_url_params();
    }

    var list = $('#gallery');
    var new_page = (page-1)*num_elements_page;
    var page_data = JSON.parse(JSON.stringify(gallery_data.slice(new_page, new_page+num_elements_page)));

    list.html('');
    for (var datum of page_data) {
        if (datum.type == 'school') {
            var listItem = $('<li></li>').addClass('collection-item');
            var schoolName = $('<p></p>').attr('href', '#').text(datum.name);
            listItem.append(schoolName);
        }
        else {
            var listItem = $('<a></a>').addClass('collection-item');
            listItem.attr('href', '/sites/'+site_slug+'/'+datum.uri+'/'+datum.id);
            listItem.text(datum.type + ': ' + datum.date);
        }

        list.append(listItem);
    }

    if (page == 1) {
        $('#first-page-gallery').addClass('disabled');
    } else {
        $('#first-page-gallery').removeClass('disabled');
    }

    if (page == page_count_gl) {
        $('#last-page-gallery').removeClass('wave-effects').addClass('disabled');
    } else {
        $('#last-page-gallery').addClass('wave-effects').removeClass('disabled');
    }

    $('.page-select-gallery').removeClass('active').addClass('wave-effects');
    $('#page-'+page+'-gallery').addClass('active').removeClass('wave-effects');
}


function get_url_params() {
    var url = new URL(window.location.href);
    datasheet_param = url.searchParams.get('datasheet');
    gallery_param = url.searchParams.get('gallery');

    datasheet_page = (datasheet_param != null ? datasheet_param : datasheet_page);
    gallery_page = (gallery_param != null ? gallery_param : gallery_page);

    if (datasheet_page > page_count_ds || datasheet_page < 1 || gallery_page > page_count_gl || gallery_page < 1) {
        datasheet_page = Math.max(1, Math.min(datasheet_page, page_count_ds));
        gallery_page = Math.max(1, Math.min(gallery_page, page_count_gl));
        update_url_params();
    }
}

function update_url_params() {
    if (history.pushState) {
        var newurl = window.location.href.split('?')[0];

        if (datasheet_page != 1) {
            newurl += '?datasheet=' + datasheet_page;
            if (gallery_page != 1) {
                newurl += '&gallery=' + gallery_page;
            }
        } else if (gallery_page != 1) {
            newurl += '?gallery=' + gallery_page;
        }

        window.history.pushState({path:newurl},'',newurl);
    }
}


$(document).ready(function () {
    // Initially sort
    get_url_params();
    filter_datasheets(datasheet_page);
    filter_gallery(gallery_page);

    var latlng = new google.maps.LatLng(loc.lat, loc.lng);
    var mapOptions = {
      zoom: 14,
      center: latlng,
      mapTypeControl: false,
      navigationControlOptions: {style: google.maps.NavigationControlStyle.SMALL},
      mapTypeId: 'roadmap'
    };
    map = new google.maps.Map($('#detail_map')[0], mapOptions);

    marker = new google.maps.Marker({
      position: loc,
      map: map,
      title: "Site Location"
    });

    // responsive function
    google.maps.event.addDomListener(window, "resize", function () {
      var center = map.getCenter();
      google.maps.event.trigger(map, "resize");
      map.setCenter(center);
    });
});
