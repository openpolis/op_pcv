function place_label(obj, r)
{
    //figure out the center point of the arc, at radius r
    var ao = -Math.PI / 2 ;
    var aa = ((obj.endAngle-obj.startAngle)/2)+obj.startAngle;
    var tx = Math.cos(aa + ao);
    var ty = Math.sin(aa + ao) ;
    tx *= r;
    ty *= r;
    return {"x": tx, "y": ty }

}


function sweep(a) {

    var i = d3.interpolate({startAngle: -90*grad, endAngle: -90*grad},a);
    return function(t) {
        return arc(i(t));
    };

}

function resize(){
    var window_width=window.innerWidth
    pie_container =$("#pie_container")
    width = pie_container.outerWidth()-(pie_container.outerWidth()*0.1);
    height= width / 1.19;

    if(width> 380)
        width=380;
    if(height>255)
        height=255;

    radius = width/4;
    outer_label_radius = radius+(radius/1.5);
    inner_label_radius = radius+(radius/1.8);
    arc_width = radius/2;

    offset_x_n = -(width/3.9 );
    offset_y_n = height -(height/4);
    offset_y_label = offset_y_n-(height/12);
    offset_y_line = offset_y_label-(height/24);

    offset_ntot= -27;
    offset_labeltot= -7;
    arc = d3.svg.arc().innerRadius(radius-arc_width).outerRadius(radius + arc_width);
}


//draws an arc in the div called div_id with the data provided
function draw_arc(div_id, data, label){

    var color = d3.scale.category20();

    if(window.innerWidth<1200)
        resize();

    var svg = d3.select("#"+div_id).
        append("svg").
        data(data).
        attr("width", width).
        attr("height",height).
        append("g").
        attr("transform","translate("+ width/2+","+(height) +")");

    var pie_chart = d3.layout.
        pie().
        sort(null).
        value(function(d) { return d.value; }).
        startAngle(-90*grad).endAngle(90*grad);

    var arcs = pie_chart(data);

    svg.selectAll("path").
        data(pie_chart(data)).
        enter().
        append("path").
        attr("d",arc).
        attr("fill",function(d, i) {
            if(data[i].label=="ADERISCONO")
                return "#65a0b8";
            else
                return "#e54442";
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
        .attr("class","big_bold_label")
        .attr("fill", "#65a0b8")
        .text(data[0].value);

    svg.append("svg:text")
        .attr("transform", "translate("+offset_x_n+",-"+offset_y_label+")")
        .attr("text-anchor", "middle")
        .text(data[0].label);


    svg.append("svg:text")
        .attr("transform", "translate("+ (-offset_x_n)+",-"+offset_y_n+")")
        .attr("text-anchor", "middle")
        .attr("class","big_bold_label")
        .attr("fill", "#e54442")
        .text(data[1].value);

    svg.append("svg:text")
        .attr("transform", "translate("+(-offset_x_n)+",-"+offset_y_label+")")
        .attr("text-anchor", "middle")
        .text(data[1].label);


}
