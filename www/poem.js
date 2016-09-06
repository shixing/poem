// the translate button
gmodel="";
gtopic="";

$('#translate-button').click(function() {
    var btn = $(this);
    btn.button('loading');
    $("#poem").html("");
    $("#config").html("");
    $("#rhyme-info").html("");
    $("#rhyme-words").html("");
    $("#pc").html("");

    var lang = $("input[name=model]:checked").val();

    var nline = $("input[name=nline]:checked").val();

    port = 8080;
    if (lang == 1){
	port = 8081;
    }

    var model = "0";
    var topic = $('#input-topic').val();
    topic = topic.replace(/ /g, "_");
    if (topic == ""){
	if (lang == 0){
	    topic = "civil_war";
	} else {
	    topic = "guerra_civil";
	}
    }

    id = Math.round(Math.random()*1000) + 1
    gmodel = model;
    gtopic = topic;

    left_time = 40;
    if (lang == 1){
	left_time = 60;
    } else {
	if (nline == "2"){
	    left_time = 14;
	} else if (nline == "4") {
	    left_time = 18;
	}
    }
    estimation = ""
    var timer = setInterval( function() {
	estimation = "["+left_time + "s] "
	$.ajax(
	    {
		url : "http://cage.isi.edu:"+port+"/api/poem_status",
		data: {id:id},
		type:"GET",
		xhrFields:{withCredentials:false},
		success: function (response_data) {
		    left_time = left_time - 2
		    $("#status").html(estimation + response_data);
		}
	    }
	);
    },2000)

    $.ajax({
	url: "http://cage.isi.edu:"+port+"/api/poem_check",
	data: {
	    topic:topic,
	    k:1,
	    model:model,
	    id:id,
	    nline:nline
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
	    $("#poem").html(jd.poem);
	    $("#config").html(jd.config);
	    $("#rhyme-info").html(jd.rhyme_info);
	    $("#rhyme-words").html(jd.rhyme_words);
	    $("#pc").html(jd.pc);
	    $("#status").html("Ready");
	}
    }).always(function (){
	btn.button('reset');
	clearInterval(timer);
    });


});
