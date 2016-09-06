// the translate button
gmodel="";
gtopic="";

function get_poem(){
    var btn = $("#translate-button");
    btn.button('loading');
    $("#poem1").html("");
    $("#poem2").html("");
    $("#config_file").html("");

    var topic = $('#input-topic').val();
    topic = topic.replace(/ /g, "_");
    if (topic == ""){
	topic = "love";
    }

    id = Math.round(Math.random()*1000) + 1

    gtopic = topic;

    var timer = setInterval( function() {
	$.ajax(
	    {
		url : "http://cage.isi.edu:8080/api/poem_status",
		data: {id:id},
		type:"GET",
		xhrFields:{withCredentials:false},
		success: function (response_data) {
		    $("#status").html(response_data);
		}
	    }
	);
    },2000)

    $.ajax({
	url: "http://cage.isi.edu:8080/api/poem_compare",
	data: {
	    topic:topic,
	    id:id
	},
	type:"GET",
	xhrFields: {
	    // The 'xhrFields' property sets additional fields on the XMLHttpRequest.
	    // This can be used to set the 'withCredentials' property.
	    // Set the value to 'true' if you'd like to pass cookies to the server.
	    // If this is enabled, your server must respond with the header
	    // 'Access-Control-Allow-Credentials: true'.
	    withCredentials: false
	},
	success: function(response_data) {
	    jd = $.parseJSON(response_data)
	    $("#poem1").html(jd.poem1);
	    $("#poem2").html(jd.poem2);
	    $("#reverse").html(jd.reverse);
	    $("#config_file").html(jd.config_file);
	    $("#topic").html(jd.topic);
	    $('#input-topic').val(jd.topic);
	    $("#status").html("Ready");
	    $('#sr').attr("disabled",false);
	    $('#sr').html("Submit");
	}
    }).always(function (){
	btn.button('reset');
	clearInterval(timer);
    });


}

function submit_result(){
    var btn = $("#sr");
    var result = $("input[name=which]:checked").val();
    poem1 = $("#poem1").html();
    poem1 = poem1.replace(/<br\/>/g,"\n");
    poem2 = $("#poem2").html();
    poem2 = poem2.replace(/<br\/>/g,"\n");
    config_file = $("#config_file").html();
    topic = $('#topic').html();
    reverse = $("#reverse").html();
    if (reverse == "1"){
	temp = poem1;
	poem1 = poem2;
	poem2 = temp;
	if (result==2){
	    result = 1;
	} else if (result == 1){
	    result = 2;
	}
    }
   

    var topic = $('#input-topic').val();
    topic = topic.replace(/ /g, "_");
    if (topic == ""){
	topic = "love";
    }

    $.ajax({
	url: "http://cage.isi.edu:8080/api/poem_submit",
	data: {
	    poem1:poem1,
	    poem2:poem2,
	    config_file:config_file,
	    result:result,
	    topic:topic
	},
	type:"GET",
	xhrFields: {
	    // The 'xhrFields' property sets additional fields on the XMLHttpRequest.
	    // This can be used to set the 'withCredentials' property.
	    // Set the value to 'true' if you'd like to pass cookies to the server.
	    // If this is enabled, your server must respond with the header
	    // 'Access-Control-Allow-Credentials: true'.
	    withCredentials: false
	},
	success: function(response_data) {
	    $("#sr").html("Done")
	    $("#sr").attr('disabled',true);
	}
    }).always(function (){
    });


}

