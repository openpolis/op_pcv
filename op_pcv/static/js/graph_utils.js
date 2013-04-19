
function sweep(a) {

    var i = d3.interpolate({startAngle: -90*grad, endAngle: -90*grad},a);
    return function(t) {
        return arc(i(t));
    };

}


//draws an arc in the div called div_id with the data provided
function draw_arc(div_id, data, label){

    var color = d3.scale.category20();

    var svg = d3.select("#"+div_id).
        append("svg").
        data(data).
        attr("width", width).
        attr("height",height).
        append("g").
        attr("transform", "translate(" + radius*1.5 + "," + (radius*1.5+100) +")");

    var pie = d3.layout.
        pie().
        value(function(d) { return d.value; }).
        startAngle(-90*grad).endAngle(90*grad);

    svg.selectAll("path").
        data(pie(data)).
        enter().
        append("path").
        attr("d",arc).
        attr("fill",function(d, i) { return color(i); }).
        transition().
        duration(500).
        attrTween("d", sweep);

    //stampa il n. di senatori/deputati totale
    svg.append("svg:text")
        .attr("text-anchor", "middle")
        .text(label[0].value + " " + label[0].label);

    var fontsize=14;
    var x_offset = -(width/3.6 );
    var y_offset = height -70;

    //stampa il n. di aderenti/ non aderenti
    svg.append("svg:text")
        .attr("transform", "translate("+x_offset+",-"+y_offset+")")
        .attr("text-anchor", "middle")
        .text(data[0].value + " " + data[0].label);


    svg.append("svg:text")
        .attr("transform", "translate("+ (-x_offset)+",-"+y_offset+")")
        .attr("text-anchor", "middle")
        .text(data[1].value + " " + data[1].label);


}
