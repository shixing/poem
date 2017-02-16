
function send_feedback(){
    setTimeout(function(){
	send_feedback_core();
    }, 100);
}

function send_feedback_core(){
    $('#rate_message').html("");
    poem_id = $("#poem_id").html();
    if (poem_id == ""){
	console.log("no poem");
	return
    }
    score = $('#rate_star').raty('score');
    console.log(poem_id);
    console.log(score);
    score_messages = ['bad','poor','ok','great','like a human'];
    score_message = "Thanks for your feedback !";
    data = {
	poem_id: poem_id,
	score:score
    };
    $.ajax({
	url: "http://"+api_host+":"+port+"/api/feedback",
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
	    $("#rate_message").html(score_message);
	    
	    if (scored == 0){
		poem_history[$("#poem").html()] = 1;
		n_regen += 1;
		$("#regen_time").html(n_regen);
		if (n_regen >= 6){
		    temp_ticket = generate_ticket();
		    $('#exp_ticket').html(temp_ticket);
		} else {
		    $('#exp_ticket').html("");
		}
	    }
	    scored = 1;
	    
	    

	}
    }).always(function (){
    });

}

function init_star(){
    $('#rate_star').css("display",'block');
    $('#rate_message').css("display",'block');
    $('#rate_star').raty({ starType: 'i', click: send_feedback });
}


function same_poem(){
    $('#rate_message').css("display",'block');
    $("#rate_message").html("You generated this poem before, please adjust style again.");
}


function before_translate(){
    $('#rate_star').css("display",'none');
    $('#rate_message').html("");
    $('#rate_message').css("display",'none');
}



