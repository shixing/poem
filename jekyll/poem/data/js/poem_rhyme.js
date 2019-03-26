api_host = window.location.hostname
port= "8080"
//global id;
var gid = 0;

function start_over(){
    $("#rhyme-words").html("");
    $("#exact-rhyme-candidates").html("");
    $("#poem_id").html("");
}

function rec_rhyme(){
    var btn = $("#rec_rhyme_button")
    btn.button('loading');
    
    before_translate();
    start_over();

    var topic = $('#input-topic').val();
    topic = topic.replace(/ /g, "_");
    if (topic == ""){
	topic = "love";
    }

    var nline = $("input[name=nline]:checked").val();

    id = Math.round(Math.random()*1000) + 1
    gid = id;
    
    //for debug
    gtopic = topic;


    $.ajax({
	url: "http://"+api_host+":8080/api/rhyme_auto",
	data: {
	    topic:topic,
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
	    rhyme_words = jd.rhyme_words;
	    rhyme_info = jd.rhyme_info;

	    $("#rhyme-words").html(rhyme_words);
	    $("#exact-rhyme-candidates").html(jd.rhyme_info);
	    $("#poem_id").html(jd.rhyme_id);


	    $("#status").html("Ready");
	    
	    init_star_rhyme();

	}
    }).always(function (){
	btn.button('reset');
    });

}


