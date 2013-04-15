
function sweep(a) {

    var i = d3.interpolate({startAngle: -90*grad, endAngle: -90*grad},a);
    return function(t) {
        return arc(i(t));
    };
}


//draws an arc in the div called div_id with the data provided
function draw_arc(div_id, data){

    var color = d3.scale.category20();

    var svg = d3.select("#"+div_id).
        append("svg").
        attr("width", width).
        attr("height",height).
        append("g").
        attr("transform", "translate(" + radius*1.5 + "," + radius*1.5 +")");



    var pie = d3.layout.pie().sort(null).startAngle(-90*grad).endAngle(90*grad);

    svg.selectAll("path").
        data(pie(data)).
        enter().
        append("path").
        attr("d",arc).
        attr("fill",function(d, i) { return color(i); }).
        transition().
        duration(500).
        attrTween("d", sweep);

}