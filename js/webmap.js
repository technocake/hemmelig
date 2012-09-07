var svgDoc = null;
var show_country = function(ctr) {    
    try { svgDoc.getElementById(ctr).style.display = 'block'; } 
    catch(e) {}
}

function get_country(ctr) {
    try {
        return svgDoc.getElementById(ctr);
    }    catch(e) {}
}


var hide_country = function(ctr) {   
    try{
        svgDoc.getElementById(ctr).style.display = 'none';  
    }
    catch(e) {}
}


var draw_hop = function (v1, v2) {
    /*
     *  1. get cx,cy of svg elements to v1 and v2
     *  2. draw line from cx,cy of v1 to cx,cy of v2
     */
     var cx1, cx2, cy1, cy2;
     var ctr1 = get_country(v1);
     var ctr2 = get_country(v2);

     /*     Getting the points      */
     cx1 = ctr1.getAttribute('cx');
     cy1 = ctr1.getAttribute('cy');
     cx2 = ctr2.getAttribute('cx');
     cy2 = ctr2.getAttribute('cy');

     /*     Drawing a line between the two points   */
     draw_line(cx1,cy1, cx2,cy2);
};

function draw_line(x0,y0, x1,y1) {

    /*  Drawing a line!     */
    $('#svgalpha').append(' <line x1="' + x0 + '" y1="' + y0 + '" x2="' + x1 + '" y2="' + y1 + '" style="stroke: black;"/> ');
}

var hide_all = function() {
    all = svgDoc.getElementsByTagName('g'); // Need a better filter here...
    for (var i = all.length - 1; i >= 0; i--) {

        if (all[i].id.length == 2) { //hacked-filter
            all[i].style.display = 'none';
        }
    }
}


 $(window).load(function () {

        // let's invite Firefox to the party.
        if (window.MozWebSocket) {
          window.WebSocket = window.MozWebSocket;
        }

        //alert("Document loaded, including graphics and embedded documents (like SVG)");
        svgDoc = document.embeds['alphasvg'].getSVGDocument();

        $('#trace_btn').click(function(e) {
            console.log('Following the path to ' + $('#destination').val());
            traceroute($('#destination').val());
        }
        );

        $('#trace_btn').click();

        //var norway = svgDoc.getElementById("NO"); //get the inner element by id
        //norway.setAttributeNS(null, 'style', 'display:block');
    });


var xmlhttp = new XMLHttpRequest();
var str = '', line;

function chr(AsciiNum) {   return String.fromCharCode(AsciiNum);   }

/*  @whattheduck:  Removes nasty non-json-friendly characters such 
 *  as newline and carriage return. 
 */
function parse(text){
    parsedText = text.replace(chr(10), "");
    return parsedText.replace(chr(13), "");

}



function ondata(data) {
    
    
    jdata = $.parseJSON(parse(data));
    for (var i = jdata.length - 1; i >= 0; i--) {
        
        console.log(jdata[i].ctr);
        show_country(jdata[i].ctr);

    }

        console.log('All data: \n' );
        console.log(jdata);

    
}

xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
        var nodes = xmlhttp.responseText;
        console.log('received response');
        ondata(nodes);
    }
}

function traceroute (destination) {
    xmlhttp.open("GET", "traceroute/" + destination, true);
    xmlhttp.send();
}

