api_host = window.location.hostname
page_source = "experiment_interactive"

var guidelines = ["Let Hafez recommend some rhyme words first","Please confirm the rhyme words by clicking \"Confirm\"","Rhyme words are ready. Let's start !<br//>NOTE: Be sure your lines end with the rhyme words in the grey boxes. "]

//global id;
var gid = 0;
var total_line = 14;
var processed_line = 0;
var poem_record;
var global_rhyme_id = 0;
var ticket = 0;
nline_onchange(4);
// disable the line input
$('input[name=nline]').prop('disabled',true)


class PoemRecord {
    constructor(topic, rhyme_id,  n){
	this.hme_flags = []; // human / machine flags
	this.poems = [];
	this.discourage_words = [];
	this.rhyme_id = rhyme_id;
	this.topic = topic
	this.n = n
	
	for (var i = 0; i < n; i ++){
	    this.hme_flags.push('E');
	    this.poems.push("");
	    this.discourage_words.push("");
	}
    }

    generate_by_human(index){ // index starts from 1
	var i = index - 1;
	this.hme_flags[i] = "H";
	this.discourage_words[i] = "";
	this.poems[i] = $("#line"+ index.toString()).val()

    }
    
    generate_by_machine(index){	// index starts from 1
	var i = index - 1;
	this.hme_flags[i] = "M";
	this.discourage_words[i] = $("#discourage"+ index.toString()).val()
	this.poems[i] = $("#line"+ index.toString()).val()
    }

    log_it(){
	$.ajax({
	url: "http://"+api_host+":8080/api/log_interactive",
	data: {
	    topic:this.topic,
	    rhyme_id:this.rhyme_id,
	    poems:JSON.stringify(this.poems),
	    discourage_words:JSON.stringify(this.discourage_words),
	    hme_flags:JSON.stringify(this.hme_flags),
	    nline:this.n,
	    source:page_source
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
	    console.log(response_data)
	}
    }).always(function (){
    });
    }

}


function nline_onchange(n){
    total_line = n;
    var oneline = `
<div class="row poem-line">

    <div class="col-lg-4">
      <input type="text" class="form-control" id="line@@" placeholder="Line #@@">
    </div>

    <div class="col-lg-2">	    
      <input type="text" class="form-control" id="rhyme@@" placeholder="Rhyme Word #@@">
    </div>

    <div class="col-lg-2">	    
      <input type="text" class="form-control" id="discourage@@" placeholder="Discourage Words #@@">
    </div>

    <div class="col-lg-3">
      <div id="bs@@" style="display:none">
    
	<button id="forward_btn@@" class="btn btn-default" type="button" data-loading-text="..." onclick="feed_history(@@,'forward')" data-toggle="tooltip" data-placement="top" title="by computer"><span class="glyphicon glyphicon-play" aria-hidden="true"></span></button>

	<button id="fast_forward_btn@@" style = "display:none" class="btn btn-default" type="button" data-loading-text="..." onclick="feed_history(@@,'fast_forward')" data-toggle="tooltip" data-placement="top" title="all by computer"><span class="glyphicon glyphicon-fast-forward" aria-hidden="true"></span></button>

	<button id="upload_btn@@" class="btn btn-default" type="button" data-loading-text="..." onclick="feed_history(@@,'upload')" data-toggle="tooltip" data-placement="top" title="by human"><span class="glyphicon glyphicon-cloud-upload" aria-hidden="true"></span></button>

      </div>

      <div id="rs@@" style="display:none">
	<button id="repeat_btn@@" class="btn btn-default" type="button" data-loading-text="..." onclick="feed_history(@@,'repeat')" data-toggle="tooltip" data-placement="top" title="regenerate by computer"><span class="glyphicon glyphicon-repeat" aria-hidden="true"></span></button>
      </div> 
    </div>
	
  </div>
`;
    temp = "";
    for (var i = 0; i<n; i += 1){
	temp += oneline.replace(/@@/g,i+1);
    }
    $("#lines").html(temp);
}



function g(i){
    $("#guideline").html(guidelines[i]);
}

function generate_ticket(){
    if (ticket != 0){
	// do nothing
    }
    else {
	r = Math.round(Math.random()*10000) + 2;
	ticket = 821 * r - 1;
	$('#ticket').html("Ticket: "+ticket.toString());	
	$('#ticket').show();
	
    }
}


function display_btn(index){
    if (processed_line < index -1){
	processed_line = index - 1;
	if (processed_line == total_line){
	    generate_ticket();
	}
    }
    for (var i = 1; i < total_line+1; i++){
	$("#bs"+ i.toString()).hide();
	if (i <= processed_line){
	    if ( i % 2 == 1){
		$("#rs"+ i.toString()).show();
	    } else {
		$("#rs"+ i.toString()).hide();
	    }
	} else {
	    $("#rs"+ i.toString()).hide();
	}
    }
    $("#bs"+ (processed_line+1).toString()).show();
    if ((processed_line + 1) % 2 == 1){
	$("#forward_btn"+ (processed_line+1).toString()).show();
	$("#upload_btn"+ (processed_line+1).toString()).hide();
    } else {
	$("#forward_btn"+ (processed_line+1).toString()).hide();
	$("#upload_btn"+ (processed_line+1).toString()).show();
    }
}


function disable_model(disable){
    //$('input[name=model]').attr("disabled",disable);
}


function clear_line_rhyme(){
    for (var i = 1; i < total_line+1; i++){
	$("#line"+ i.toString()).val("")
	$("#rhyme"+ i.toString()).val("")
	$("#discourage"+ i.toString()).val("")
	$("#rhyme"+ i.toString()).prop('disabled',false);
    }
}

function start_over()
{
    processed_line = 0;
    clear_line_rhyme();
    g(0);
    display_btn(0);
    $("#confirm_button").prop('disabled',true);
    disable_model(false);
    $('#ticket').hide();
    ticket = 0;
}


function confirm_rhyme(){
    var btn = $("#confirm_button");
    //btn.button('loading');
    
    id = gid ;
    var words = []
    for (var i = 1; i < total_line+1; i++){
	word = $("#rhyme"+ i.toString()).val();
	words.push(word);
    }
    words_str = JSON.stringify(words)


    var timer = setInterval( function() {
	$.ajax(
	    {
		url : "http://"+api_host+":8080/api/poem_status",
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
	url: "http://"+api_host+":8080/api/confirm",
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

	    for (var i = 1; i < total_line+1; i++){
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

    id = Math.round(Math.random()*10000) + 1
    gid = id;
    
    //for debug
    gtopic = topic;

    var timer = setInterval( function() {
	$.ajax(
	    {
		url : "http://"+api_host+":8080/api/poem_status",
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
	url: "http://"+api_host+":8080/api/rhyme",
	data: {
	    topic:topic,
	    id:id,
	    nline:total_line,
	    source:page_source
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
	    
	    global_rhyme_id = jd.rhyme_id;

	    poem_record = new PoemRecord(topic, global_rhyme_id, total_line);

	    for (var i = 1; i < total_line+1; i++){
		$("#rhyme"+ i.toString()).val(rhymes[i-1])
	    }
	    g(1);
	    $("#confirm_button").prop("disabled",false);
	    $("#status").html("Ready");

	    //confirm button pressed here
	    for (var i = 1; i < total_line+1; i++){
		$("#rhyme"+ i.toString()).prop("disabled",true);
	    }

	    disable_model(true);
	    g(2);
	    display_btn(1);
	    $("#status").html("Ready");

	}
    }).always(function (){
	btn.button('reset');
	clearInterval(timer);
    });

}


function feed_history(index, next_action){
    model = 0;
    action = "feed_history";
    id = gid;
    
    words = [];
    for (var i = 1; i < index; i++){
	line = $("#line"+i.toString()).val();
	words.push(line);
    }
    words_json = JSON.stringify(words);

    var btn = $("#"+next_action+"_btn"+index.toString());
    btn.button('loading');

    $.ajax({
	url: "http://"+api_host+":8080/api/poem_interactive",
	data: {
	    model:model,
	    action:action,
	    line:index,
	    words:words_json,
	    id:id
	},
	type:"GET",
	xhrFields: {
	    withCredentials: false
	},
	success: function(response_data) {
	    if (next_action == "forward"){
		forward(index);
	    } else if (next_action == "fast_forward"){
		fast_forward(index);
	    } else if (next_action == "upload"){
		upload(index);
	    } else if (next_action == "repeat"){
		forward(index, "repeat");
	    }

	 
	}
    }).fail(function (){
	btn.button('reset');
    });

}


function forward(index, btn_name = "forward"){ // index starts from one
    var btn = $("#"+btn_name+"_btn"+index.toString());
    console.log(btn_name);
    btn.button('loading');

    //model = $("input[name=model]:checked").val();
    model = 0;
    action = "fsaline";

    id = gid;

    //read the discourage words here
    
    discourage_words = $("#discourage"+index.toString()).val();
    
    var cword = -5.0;
    var reps = 0.0;
    var allit = 0.0;
    var wordlen = 0.0;
    var topical = 1.0;
    var mono = -5;
    var sentiment = 0;
    var concrete = 0;
    var discourage_weight = -5;


    var timer = setInterval( function() {
	$.ajax(
	    {
		url : "http://"+api_host+":8080/api/poem_status",
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
	url: "http://"+api_host+":8080/api/poem_interactive",
	data: {
	    model:model,
	    action:action,
	    line:index,
	    words:"",
	    discourage_words:discourage_words,
	    discourage_weight:discourage_weight,
	    cword:cword,
	    reps:reps,
	    allit:allit,
	    topical:topical,
	    wordlen:wordlen,
	    mono:mono,
	    sentiment:sentiment,
	    concrete:concrete,
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
	    
	    poem_record.generate_by_machine(index);
	    poem_record.log_it();


	}
    }).always(function (){
	btn.button('reset');
	clearInterval(timer);
    });
}

function fast_forward(index){
    var btn = $("#fast_forward_btn"+index.toString());
    btn.button('loading');

    //model = $("input[name=model]:checked").val();
    model = 0;
    action = "fsa";

    id = gid;
    
    var timer = setInterval( function() {
	$.ajax(
	    {
		url : "http://"+api_host+":8080/api/poem_status",
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
	url: "http://"+api_host+":8080/api/poem_interactive",
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
	    for (var i = index; i<=total_line; i+=1){
		$("#line"+i.toString()).val(poems[i-index]);
	    }
	    display_btn(total_line+1);
	}
    }).always(function (){
	btn.button('reset');
	clearInterval(timer);
    });

}

function upload(index){
    var btn = $("#upload_btn"+index.toString());
    btn.button('loading');

    //model = $("input[name=model]:checked").val();
    model = 0;
    action = "words";

    id = gid;
    words = $("#line"+index.toString()).val();
    
    var timer = setInterval( function() {
	$.ajax(
	    {
		url : "http://"+api_host+":8080/api/poem_status",
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
	url: "http://"+api_host+":8080/api/poem_interactive",
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

	    poem_record.generate_by_human(index);
	    poem_record.log_it();

	}
    }).always(function (){
	btn.button('reset');
	clearInterval(timer);
    });

}
