//pie chart
var grad=Math.PI/180;
var width = 380;
var height = 255;
var radius = 100;
var outer_label_radius = radius+(radius/1.5);
var inner_label_radius = radius+(radius/1.8);
var arc_width = 50;


var offset_x_n = -(width/3.9 );
var offset_y_n = height -60;
var offset_y_label = offset_y_n-20;
var offset_y_line = offset_y_label-10;

var offset_ntot= -27;
var offset_labeltot= -7;

var arc = d3.svg.arc().innerRadius(radius-(arc_width/1.2)).outerRadius(radius + (arc_width*1.2));


