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

    width=(window.innerWidth/2)-20;
    offset_x_n = -(width/3 );
    radius = width/4;
    outer_label_radius = radius+(radius/1.5);
    inner_label_radius = radius+(radius/1.8);
    arc_width = radius/2;

    offset_x_n = -(width/3 );
    offset_y_n = height -(height/4);
    offset_y_label = offset_y_n-(height/12);
    offset_y_line = offset_y_label-(height/24);

    offset_ntot= -25;
    offset_labeltot= -3;
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
        attr("transform", "translate(" + radius*1.8 + "," + (radius*1.5+100) +")");

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
        .attr("class","big_bold_label")
        .text(data[0].value);

    svg.append("svg:text")
        .attr("transform", "translate("+offset_x_n+",-"+offset_y_label+")")
        .attr("text-anchor", "middle")
        .text(data[0].label);


    svg.append("svg:text")
        .attr("transform", "translate("+ (-offset_x_n)+",-"+offset_y_n+")")
        .attr("text-anchor", "middle")
        .attr("class","big_bold_label")
        .text(data[1].value);

    svg.append("svg:text")
        .attr("transform", "translate("+(-offset_x_n)+",-"+offset_y_label+")")
        .attr("text-anchor", "middle")
        .text(data[1].label);


    //aggiunge le linee di connessione fra grafico e labels
    var connection_lines=[];

    connection_lines[0]={
        x1:offset_x_n,
        y1:-offset_y_line
    };
    connection_lines[1]={
        x1:-offset_x_n,
        y1:-offset_y_line
    };

    connection_lines[2]={};
    connection_lines[3]={};
    var i,temp;

    for( i=0;i<2;i++){
        temp = place_label(arcs[i], outer_label_radius);
        connection_lines[i].x2=temp.x;
        connection_lines[i].y2=temp.y;
        connection_lines[i+2].x1 = temp.x;
        connection_lines[i+2].y1 = temp.y;
    }

    for(i=2; i<4; i++){
        temp = place_label(arcs[i-2], inner_label_radius);
        connection_lines[i].x2=temp.x;
        connection_lines[i].y2=temp.y;
    }

    svg.selectAll().
        data(connection_lines).
        sort(null).
        enter().
        append("line").
        attr("x1",function(d) { return d.x1;}).
        attr("y1",function(d) { return d.y1;}).
        attr("x2",function(d) { return d.x2;}).
        attr("y2",function(d) { return d.y2;}).
        attr("stroke","black").
        attr("class","connection-line");

}
