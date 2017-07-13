/***************************************************
        Adjust the card size
        Associated with: ajustCardHeight, getHeight
***************************************************/
var adjustCardSize = function adjustCardSize() {
  var countDivs = $('div.count-row > div');
  if ($(window).width() < 880) {
    if (countDivs.hasClass("s6")) {
      countDivs.removeClass("s6").addClass("s12");
    }
    adjustCardHeight(false);
  }
  else {
    if (countDivs.hasClass("s12")) {
      countDivs.removeClass("s12").addClass("s6");
    }
    adjustCardHeight(true);
  }
}

var adjustCardHeight = function adjustCardHeight(matchHeight) {
  if (matchHeight) {
    $('div.count-row').each(function() {

      var countDivs = $(this).find('div.card');
      var height0 = getHeight(countDivs[0]);
      var height1 = getHeight(countDivs[1]);
      var height = Math.max(height0, height1);

      countDivs.each(function() {
        $(this).height(height);
      })
    });
  } else {
    console.log("HELLO");
    $('div.count').each(function() {
      var height = getHeight(this);
      console.log(height);
      $(this).height(getHeight(this));
    });
  }
}

var getHeight = function getHeight(elem) {
  height = 0;
  $(elem).children().each(function() {
    height += $(this).height();
  });
  return height + 45;
}
/***************************************************
        Document ready & Document related
***************************************************/

$(document).ready(function() {
  adjustCardSize();
  $('#schools_table').DataTable({
    bLengthChange: false,
    "pageLength": 13
  });
  $('#sites_table').DataTable({
    bLengthChange: false,
    "pageLength": 13
  })
  $('.datepicker').pickadate({
    today: '',
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 100, // Creates a dropdown of 15 years to control year
    max: true, // set max to today
    format: 'yyyy-mm-dd',
  });

  $('input#schools-btn').click(function() {
    console.log("HELLO");
    $('div.count-row').hide();
    $('div.schools').show();
  });
  $('input#sites-btn').click(function() {
    $('div.count-row').hide();
    $('div.sites').show();
  });
  $('input.back').click(function() {
    $('div.schools, div.sites').hide();
    $('div.count-row').show();
  })
});

$(window).resize(function () {
    adjustCardSize();
})
