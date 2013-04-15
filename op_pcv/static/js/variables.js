//pie chart
var grad=Math.PI/180;
var width = 250;
var height = 180;
var radius = 100;
var arc = d3.svg.arc().innerRadius(radius - (radius/3)).outerRadius(radius - ((radius - radius/3)/10));
//pie chart labelling
var label_array=[];
label_array["Adesione"]={};
label_array["Adesione"][0] = 'Non risponde';
label_array["Adesione"][1] = 'Aderisce';
label_array["Adesione"][2] = 'Non Aderisce';
label_array["Parlamentari"]={};
label_array["Parlamentari"][0] = 'Deputati';
label_array["Parlamentari"][1] = 'Senatori';

