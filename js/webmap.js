var svgDoc = null;
var show_country = function(ctr) {     svgDoc.getElementById(ctr).style.display = 'block';  }
var hide_country = function(ctr) {     svgDoc.getElementById(ctr).style.display = 'none';   }
var hide_all = function() {
    all = svgDoc.getElementsByTagName('g'); // Need a better filter here...
    for (var i = all.length - 1; i >= 0; i--) {

        if (all[i].id.length == 2) { //hacked-filter
            all[i].style.display = 'none';
        }
    };
}


 $(window).load(function () {

        // let's invite Firefox to the party.
        if (window.MozWebSocket) {
          window.WebSocket = window.MozWebSocket;
        }

        //alert("Document loaded, including graphics and embedded documents (like SVG)");
        svgDoc = document.embeds['alphasvg'].getSVGDocument();

        $('#trace_btn').click(function(e) {
            console.log('Following the path to ' + $('#destination').val())
            traceroute($('#destination').val());
        }
        );

        //var norway = svgDoc.getElementById("NO"); //get the inner element by id
        //norway.setAttributeNS(null, 'style', 'display:block');
    });


var xmlhttp = new XMLHttpRequest();
var str = '', line;

function ondata(chunk) {
    str += chunk
    while ( (line = str.split('\n', 1))) {
        line = $.parseJSON(line);
        show_country(line['ctr']);
        console.log(chunk)
    }
}

xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 3 && xmlhttp.status == 200){
        var nodes = xmlhttp.responseText;
        console.log('received response');
        ondata(nodes);
    }
}

function traceroute (destination) {
    xmlhttp.open("GET", "traceroute/" + destination, true);
    xmlhttp.send();
}

