var zones = window.zones_json;
var margin = {top: 20, right: 20, bottom:40, left:20};
var dimension = {maxWidth: 800, HtoWRatio: 0.8};
$(function() {
    createGraph();
});

$(document).resize(function() {
    createGraph();
});

var createGraph = function createGraph() {
    var width = Math.min($('.inner-wrap').width() - 200, dimension.maxWidth) + margin.left + margin.right;
    var height = width * dimension.HtoWRatio + margin.top + margin.bottom;

}
