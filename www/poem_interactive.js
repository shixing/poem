var guidelines = ["Let Hafez recommend some rhyme words first","Please confirm the rhyme words and beam size by clicking \"Confirm\"","Rhyme words and beam size are confirmed. Let's start !"]

//global id;
var gid = 0;

function g(i){
    $("#guideline").html(guidelines[i]);
}

function display_btn(index){
    for (var i = 1; i < 15; i++){
	$("#bs"+ i.toString()).hide();
    }
    $("#bs"+ index.toString()).show();
}

function disable_model(disable){
    $('input[name=model]').attr("disabled",disable);
}

function clear_line_rhyme(){
    for (var i = 1; i < 15; i++){
	$("#line"+ i.toString()).val("")
	$("#rhyme"+ i.toString()).val("")
	$("#rhyme"+ i.toString()).prop('disabled',false);
    }
}

function start_over()
{
    clear_line_rhyme();
    g(0);
    display_btn(0);
    $("#confirm_button").prop('disabled',true);
    disable_model(false);

}

function confirm_rhyme(){
    var btn = $("#confirm_button");
    //btn.button('loading');
    
    id = gid ;
    var words = []
    for (var i = 1; i < 15; i++){
	word = $("#rhyme"+ i.toString()).val();
	words.push(word);
    }
    words_str = JSON.stringify(words)


    var timer = setInterval( function() {
	$.ajax(
	    {
		url : "http://cage.isi.edu:8081/api/poem_status",
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
	url: "http://cage.isi.edu:8081/api/confirm",
	data: {
	    words:words_str,
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

	    for (var i = 1; i < 15; i++){
		$("#rhyme"+ i.toString()).prop("disabled",true);
	    }
	    btn.prop("disabled",true);
	    disable_model(true);
	    
	    g(2);
	    display_btn(1);

	    
	    $("#status").html("Ready");

	    
	}
    }).always(function (){
	clearInterval(timer);
    });

}

function rec_rhyme(){
    var btn = $("#rec_rhyme_button")
    btn.button('loading');
    
    start_over();

    var topic = $('#input-topic').val();
    topic = topic.replace(/ /g, "_");
    if (topic == ""){
	topic = "love";
    }

    id = Math.round(Math.random()*1000) + 1
    gid = id;
    
    //for debug
    gtopic = topic;

    var timer = setInterval( function() {
	$.ajax(
	    {
		url : "http://cage.isi.edu:8081/api/poem_status",
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
	url: "http://cage.isi.edu:8081/api/rhyme",
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
	    rhymes = jd.rhyme_words;
	    
	    for (var i = 1; i < 15; i++){
		$("#rhyme"+ i.toString()).val(rhymes[i-1])
	    }
	    g(1);
	    $("#confirm_button").prop("disabled",false);
	    $("#status").html("Ready");
	}
    }).always(function (){
	btn.button('reset');
	clearInterval(timer);
    });

}

function forward(index){
    var btn = $("#forward_btn"+index.toString());
    btn.button('loading');

    model = $("input[name=model]:checked").val();
    action = "fsaline";

    id = gid;
    
    var timer = setInterval( function() {
	$.ajax(
	    {
		url : "http://cage.isi.edu:8081/api/poem_status",
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
	url: "http://cage.isi.edu:8081/api/poem_interactive",
	data: {
	    model:model,
	    action:action,
	    line:index,
	    words:"",
	    id:id
	},
	type:"GET",
	xhrFields: {
	    withCredentials: false
	},
	success: function(response_data) {
	    //[Here]
	    clearInterval(timer);
	    $("#status").html("Ready");
	    jd = $.parseJSON(response_data)
	    poems = jd.poem;
	    $("#line"+index.toString()).val(poems[0])
	    display_btn(index+1);
	}
    }).always(function (){
	btn.button('reset');
	clearInterval(timer);
    });
}

function fast_forward(index){
    var btn = $("#fast_forward_btn"+index.toString());
    btn.button('loading');

    model = $("input[name=model]:checked").val();
    action = "fsa";

    id = gid;
    
    var timer = setInterval( function() {
	$.ajax(
	    {
		url : "http://cage.isi.edu:8081/api/poem_status",
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
	url: "http://cage.isi.edu:8081/api/poem_interactive",
	data: {
	    model:model,
	    action:action,
	    line:index,
	    words:"",
	    id:id
	},
	type:"GET",
	xhrFields: {
	    withCredentials: false
	},
	success: function(response_data) {
	    //[Here]
	    clearInterval(timer);
	    $("#status").html("Ready");
	    jd = $.parseJSON(response_data)
	    poems = jd.poem;
	    for (var i = index; i<=14; i+=1){
		$("#line"+i.toString()).val(poems[i-index]);
	    }
	    display_btn(0);
	}
    }).always(function (){
	btn.button('reset');
	clearInterval(timer);
    });

}

function upload(index){
    var btn = $("#upload_btn"+index.toString());
    btn.button('loading');

    model = $("input[name=model]:checked").val();
    action = "words";

    id = gid;
    words = $("#line"+index.toString()).val();
    
    var timer = setInterval( function() {
	$.ajax(
	    {
		url : "http://cage.isi.edu:8081/api/poem_status",
		data: {id:id},
		type:"GET",
		xhrFields:{withCredentials:false},
		success: function (response_data) {
		    $("#status").html(response_data);
		}
	    }
	);
    },2000);

    $.ajax({
	url: "http://cage.isi.edu:8081/api/poem_interactive",
	data: {
	    model:model,
	    action:action,
	    line:index,
	    words:words,
	    id:id
	},
	type:"GET",
	xhrFields: {
	    withCredentials: false
	},
	success: function(response_data) {
	    //[Here]
	    clearInterval(timer);
	    $("#status").html("Ready");
	    display_btn(index+1);
	}
    }).always(function (){
	btn.button('reset');
	clearInterval(timer);
    });

}
