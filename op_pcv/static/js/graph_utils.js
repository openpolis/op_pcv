
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
        attr("transform", "translate(" + radius*1.8 + "," + (radius*1.5+100) +")");

    var pie = d3.layout.
        pie().
        sort(null).
        value(function(d) { return d.value; }).
        startAngle(-90*grad).endAngle(90*grad);

    svg.selectAll("path").
        data(pie(data)).
        enter().
        append("path").
        attr("d",arc).
        attr("fill",function(d, i) {
            if(data[i].label=="ADERISCONO")
                return "#60b887";
            else
                return "#ff7e79";
        }).
        attr("stroke", "white").
        attr("stroke-width", "4px").
        transition().
        duration(500).
        attrTween("d", sweep);

    //stampa il n. di senatori/deputati totale
    svg.append("svg:text")
        .attr("text-anchor", "middle")
        .attr("class","bold_label")
        .attr("transform", "translate(0,"+offset_ntot+")")
        .text(label[0].value);
    //stampa  la label associata ai totali
    svg.append("svg:text")
        .attr("transform", "translate(0,"+offset_labeltot+")")
        .attr("text-anchor", "middle")
        .text( label[0].label);

    //stampa il n. di aderenti/ non aderenti
    svg.append("svg:text")
        .attr("transform", "translate("+offset_x_n+",-"+offset_y_n+")")
        .attr("text-anchor", "middle")
        .attr("class","bold_label")
        .text(data[0].value);

    svg.append("svg:text")
        .attr("transform", "translate("+offset_x_n+",-"+offset_y_label+")")
        .attr("text-anchor", "middle")
        .text(data[0].label);


    svg.append("svg:text")
        .attr("transform", "translate("+ (-offset_x_n)+",-"+offset_y_n+")")
        .attr("text-anchor", "middle")
        .attr("class","bold_label")
        .text(data[1].value);

    svg.append("svg:text")
        .attr("transform", "translate("+(-offset_x_n)+",-"+offset_y_label+")")
        .attr("text-anchor", "middle")
        .text(data[1].label);



}
