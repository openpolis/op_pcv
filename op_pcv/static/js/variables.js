//pie chart
var grad=Math.PI/180;
var width = 350;
var height = 260;
var radius = 100;
var arc_width = 50;


var offset_x_n = -(width/3.6 );
var offset_y_n = height -70;
var offset_y_label = offset_y_n-20;

var offset_ntot= -25;
var offset_labeltot= -3;


var arc = d3.svg.arc().innerRadius(radius-arc_width).outerRadius(radius + arc_width);


