$(function() {
    if (window.birthdate) {
        checkBirthdayError();
    }
    setupDatePick();

    var dates = $('div.hidden-date input').toArray();
    dates.forEach(function(date) {
        prefillDate(date);
        disableDay($(date).parent().parent());
    });
    $('div.date select').change(function() {
        showDatePick($(this).parent().parent().parent());
        disableDay($(this).parent().parent().parent());
    });
    $('form').submit(function(e) {
        var dates = $('div.hidden-date input').toArray();
        dates.forEach(function(date) {
            var parent = $(date).parent().parent();
            var day = parent.find('select.day').toArray()[0].value;
            var month = parent.find('select.month').toArray()[0].value;
            var year = parent.find('select.year').toArray()[0].value;
            var string = year + "-" + month + "-" + day;
            date.value = string;
        })

    });
});

var checkBirthdayError = function checkBirthdayError() {
    var birthdayError = $('div.hidden-date ul.errorlist li');
    var error;
    if (birthdayError.length > 0) {
        error = birthdayError.text();
    }
    $('strong.birthdate-error').text(error);
}

var prefillDate = function prefillDate(date) {
    dateVal = date.value;
    var parent = $(date).parent().parent();
    var dateSeg = dateVal.split('-');
    var year = parseInt(dateSeg[0]).toString();
    var month = parseInt(dateSeg[1]).toString();
    var day = parseInt(dateSeg[2]).toString();
    if (year === "") {
        parent.find('select.year option').toArray()[0].selected = true;
    }
    else {
        parent.find('select.year option').each(function() {
            if (this.value === year) {
                this.selected = true;
            }
        });
    }
    if (month === "") {
        parent.find('select.month option').toArray()[0].selected = true;
    }
    else {
        parent.find('select.month option').each(function() {
            if (this.value === month) {
                this.selected = true;
            }
        });
    }
    if (day === "") {
        parent.find('select.day option').toArray()[0].selected = true;
    }
    else {
        parent.find('select.day option').each(function() {
            if (this.text === day) {
                this.selected = true;
            }
        });
    }
    if (parent.find('ul.errorlist').length > 0) {
        showErrors(parent);
    }
}

var showErrors = function showErrors(parent) {
    var dateErrors = [];
    if (parent.find('select.day').toArray()[0].value === "") {
        dateErrors.push('day');
    }
    if (parent.find('select.month').toArray()[0].value === "") {
        dateErrors.push('month');
    }
    if (parent.find('select.year').toArray()[0].value === "") {
        dateErrors.push('year');
    }
    dateErrors.forEach(function(str) {
        parent.find('div.' + str +' strong').text("This field is required");
    });
}

var showDatePick = function showDatePick(parent) {
    parent.find('div.date select option').show();
}

var disableDay = function disableDay(parent) {
    var year = getYear(parent);
    var month = getMonth(parent);
    var day = getDay(parent);
    var yearInt = parseInt(year);
    var monthInt = parseInt(month);
    var dayInt = parseInt(day);

    var date = new Date();
    var thisYear = date.getFullYear();
    var thisMonth = date.getMonth() + 1;
    var today = date.getDate()
    var max = 0;
    if (year !== "" && yearInt === thisYear) {
        parent.find('select.month option').each(function(i) {
            var val = this.value;
            if (val > thisMonth) {
                $(this).hide();
            }
        });
        if (monthInt > thisMonth) {
            parent.find('select.month option').toArray()[0].selected = true;
            parent.find('select.day option').toArray()[0].selected = true;
        }
        if (monthInt == thisMonth) {
            max = today;
        }
        if (monthInt < thisMonth) {
            max = getMaxDate(monthInt, yearInt);
        }
    }
    else if (month !== "" && yearInt !== thisYear) {
        max = getMaxDate(monthInt, yearInt);
    }
    if (dayInt > max) {
        parent.find('select.day option').toArray()[0].selected = true;
    }
    parent.find('select.day option').each(function(i) {
        var val = this.value;
        if (val > max) {
            $(this).hide();
        }
    });
}

var getMaxDate = function getMaxDate(monthInt, yearInt) {
    var max;
    if (monthInt === 1 || monthInt === 3 || monthInt === 5 || monthInt === 7
      || monthInt === 8 || monthInt === 10 || monthInt === 12) {
        max = 31;
    }
    else if (monthInt === 4 || monthInt === 6 || monthInt === 9 || monthInt === 11) {
        max = 30;
    }
    else {
        max = 29;
        if (!isNaN(yearInt) && yearInt % 4 !== 0) {
            max--;
        }
    }
    return max;
}

var getYear = function getYear(parent) {
    return parent.find('select.year').toArray()[0].value;
}

var getMonth = function getMonth(parent) {
    var month = parent.find('select.month').toArray()[0].value;
    if (parseInt(month) < 10) {
        month = "0" + month;
    }
    return month;
}

var getDay = function getDay(parent) {
    var day = parent.find('select.day').toArray()[0].value;
    if (parseInt(day) < 10) {
        day = "0" + day;
    }
    return day;
}

var setupDatePick = function setupDatePick() {
    var date = new Date();
    startingYear = window.birthdate ? 1900 : 1980;
    for (var i = date.getFullYear(); i >= startingYear; i--) {
        createSelect("year", i, i.toString());
    }
    for (var i = 1; i <= 31; i++) {
        createSelect("day", i, i.toString());
    }
    createSelect("month", 1, "January");
    createSelect("month", 2, "February");
    createSelect("month", 3, "March");
    createSelect("month", 4, "April");
    createSelect("month", 5, "May");
    createSelect("month", 6, "June");
    createSelect("month", 7, "July");
    createSelect("month", 8, "August");
    createSelect("month", 9, "September");
    createSelect("month", 10, "October");
    createSelect("month", 11, "November");
    createSelect("month", 12, "December");
}

var createSelect = function createSelect(field, value, text) {
    var select = $("select." + field);
    var option = $("<option value=" + value + ">" + text + "</option>");
    select.append(option);
}
