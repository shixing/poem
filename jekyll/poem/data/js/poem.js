// the translate button
gmodel="";
gtopic="";
api_host = "vivaldi.isi.edu"

$('#translate-button').click(function() {

    before_translate();

    var btn = $(this);
    btn.button('loading');
    $("#poem").html("");

    var lang = "0"; // for english

    var nline = "4"; // 4 lines

    port = 8080;

    var model = "0";
    var topic = $('#input-topic').val();
    topic = topic.replace(/ /g, "_");
    if (topic == ""){
	topic = "civil_war";
    }

    id = Math.round(Math.random()*10000) + 1
    gmodel = model;
    gtopic = topic;

    //style
    var encourage_words = "";
    var disencourage_words = "";
    var enc_weight = 0.0;
    var cword = -5.0;
    var reps = 0.0;
    var allit = 0.0;
    var wordlen = 0.0;
    var topical = 1.0;
    var mono = -5;
    var sentiment = 0;
    var concrete = 0;
    var is_default = 1;
    var source = "auto";

    eng_data = {
	    topic:topic,
	    k:1,
	    model:model,
	    id:id,
	    nline:nline,
	    encourage_words:encourage_words,
	    disencourage_words:disencourage_words,
	    enc_weight:enc_weight,
	    cword:cword,
	    reps:reps,
	    allit:allit,
	topical:topical,
	    wordlen:wordlen,
	    mono:mono,
	sentiment:sentiment,
	concrete:concrete,
	is_default:is_default,
	source:source
    };
    data = eng_data;
    left_time = 2;
    estimation = ""
    var timer = setInterval( function() {
	estimation = "["+left_time + "s] "
	$.ajax(
	    {
		url : "http://"+api_host+":"+port+"/api/poem_status",
		data: {id:id},
		type:"GET",
		xhrFields:{withCredentials:false},
		success: function (response_data) {
		    left_time = left_time - 1
		    $("#status").html(estimation + response_data);
		}
	    }
	);
    },1000)

    $.ajax({
	url: "http://"+api_host+":"+port+"/api/poem_check",
	data: data,
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

	    jd = $.parseJSON(response_data);
	    $("#poem").html(jd.poem);
	    $("#npoem").html(jd.n_poem);
	    $("#npoem_alexa").html(jd.n_poem_alexa);
	    $("#poem_id").html(jd.poem_id);
	    $("#status").html("Ready");
	    init_star();
	}
    }).always(function (){
	btn.button('reset');
	clearInterval(timer);
    });

});
