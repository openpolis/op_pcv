
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
        data([data]).
        attr("width", width).
        attr("height",height).
        append("g").
        attr("transform", "translate(" + radius*1.5 + "," + radius*1.5 +")");

    var pie = d3.layout.pie().
        value(function(d) { return d.value; }).startAngle(-90*grad).endAngle(90*grad);

    svg.selectAll("path").
        data(pie(data)).
        enter().
        append("path").
        attr("d",arc).
        attr("fill",function(d, i) { return color(i); }).
        attr("transform", function(d) {                    //set the label's origin to the center of the arc
            //we have to make sure to set these before calling arc.centroid
            d.innerRadius = 0;
            d.outerRadius = 100;
            return "translate(" + arc.centroid(d) + ")";        //this gives us a pair of coordinates like [50, 50]
        }).
        attr("text-anchor", "middle")                          //center the text on it's origin
        .text(function(d, i) { return data[i].label; }).
        transition().
        duration(500).
        attrTween("d", sweep);

//    svg.selectAll("path").append("svg:text")                                     //add a label to each slice
//        .attr("transform", function(d) {                    //set the label's origin to the center of the arc
//            //we have to make sure to set these before calling arc.centroid
//            d.innerRadius = 0;
//            d.outerRadius = 100;
//            return "translate(" + arc.centroid(d) + ")";        //this gives us a pair of coordinates like [50, 50]
//        })
//        .attr("text-anchor", "middle")                          //center the text on it's origin
//        .text(function(d, i) { return data[i].label; });        //get the label from our original data array
//
//}