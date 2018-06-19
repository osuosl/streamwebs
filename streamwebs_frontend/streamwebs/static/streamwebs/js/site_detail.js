
function initializeMap() {
    // Iniitalize Google Map
    var latlng = new google.maps.LatLng(loc.lat, loc.lng);

    var mapOptions = {
        zoom: 14,
        center: latlng,
        mapTypeControl: false,
        navigationControlOptions: {style: google.maps.NavigationControlStyle.SMALL},
        mapTypeId: 'roadmap'
    };

    var map = new google.maps.Map($('#detail_map')[0], mapOptions);

    var marker = new google.maps.Marker({
        position: loc,
        map: map,
        title: site_name,
    });

    // responsive function
    google.maps.event.addDomListener(window, "resize", function () {
        var center = map.getCenter();
        google.maps.event.trigger(map, "resize");
        map.setCenter(center);
    });
}


function updateDimension() {
    // Update dimension of grid for page image and Google Map
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
    // Center image based on ratio
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
    // Filter datasheets shown

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
    // Filter gallery shown

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
    // Microsoft edge refuses to support modern web standards.
    // So URL.searchParams is reimplemented here.

    var datasheet_param = null;
    var gallery_param = null;
    var url = window.location.href;

    queryString = url.split("?")[1];

    if(queryString != null) {
        parameters = queryString.split("&");
        searchParams = {};

        for (var i = 0; i < parameters.length; i ++) {
            param = parameters[i];

            key = param.split("=")[0];
            value = param.split("=")[1];

            searchParams[key] = value;
        }

        datasheet_param = searchParams['datasheet'];
        gallery_param = searchParams['gallery'];
    }

    datasheet_page = (datasheet_param != null ? datasheet_param : 1);
    gallery_page = (gallery_param != null ? gallery_param : 1);

    if (datasheet_page > page_count_ds || datasheet_page < 1) {
        datasheet_page = 1;
    }
    if (gallery_page > page_count_gl || gallery_page < 1) {
        gallery_page = 1;
    }
}


function update_url_params() {
    // Update the url query parameters
    if (typeof window.history.pushState === "function") {

        var newurl = window.location.href.split('?')[0];

        if (datasheet_page != 1 || gallery_page != 1) {
            newurl += '?'
            if (datasheet_page != 1) {
                newurl += 'datasheet=' + datasheet_page;
            }
            if (gallery_page != 1) {
                newurl += '&gallery=' + gallery_page;
            }
        }
    }
    window.history.pushState({path:newurl},'',newurl);
}


function addButtonClickEvents() {
    // Add and export buttons
    $("#export_data_button").on("click", function(e){
        if (export_menu_hidden){
            $("#export_data").slideDown(500);
        } else {
            $("#export_data").slideUp(500);
        }
        export_menu_hidden = !export_menu_hidden;
    });

    $("#add_datasheet_button").on("click", function(){
        if (add_datasheet_menu_hidden){
            $("#add_datasheet_types").slideDown(500);
        } else {
            $("#add_datasheet_types").slideUp(500);
        }
        add_datasheet_menu_hidden = !add_datasheet_menu_hidden;
    });

    $("#add_gallery_item_button").on("click", function(){
        if (add_gallery_menu_hidden){
            $("#add_gallery_item_types").slideDown(500);
        } else {
            $("#add_gallery_item_types").slideUp(500);
        }
        add_gallery_menu_hidden = !add_gallery_menu_hidden;
    });
}


function addPageClickEvents() {
    $('li.page-select-datasheet').on("click", function(e) {
        datasheet_page = e.target.innerHTML;
        update_url_params(datasheet_page, gallery_page);
    });
    $('li.page-select-gallery').on("click", function(e) {
        gallery_page = e.target.innerHTML;
        update_url_params(datasheet_page, gallery_page);
    });
}


/* Main functions below */

$(document).ready(function () {
    // update dimension of grid (images & Google Map)
    updateDimension();
    // initialize Google Map
    initializeMap();
    // add click events for Add datasheets, export, & add gallery
    addButtonClickEvents();
    // add click events for pagination page number buttons
    addPageClickEvents();
    // Get the datasheets and gallery page number
    get_url_params();
    // Create datasheet and gallery table based on page number
    filter_datasheets(datasheet_page);
    filter_gallery(gallery_page);
});

$(window).on("resize", function() {
    updateDimension();
})

$(window).on("popstate", function(e) {
    // Whenever click "back" button on browser, reload page number
    get_url_params();
    filter_datasheets(datasheet_page);
    filter_gallery(gallery_page);
})
