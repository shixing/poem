api_host = "vivaldi.isi.edu"

var guidelines = ["Let Hafez recommend some rhyme words first","Please confirm the rhyme words by clicking \"Confirm\"","Rhyme words are ready. Let's start !<br//>NOTE: Be sure your lines end with the rhyme words in the grey boxes. "]

//global id;
var gid = 0;
var total_line = 14;
var processed_line = 0;
nline_onchange(4);


class Poem {
    constructor(rhyme_id){
	this.hm_flags = []; // human / machine flags
	this.poems = [];
	this.disencourage_words = [];
	this.rhyme_id = rhyme_id;
    }

    log_it(){
	// just log it; 
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

	<button id="fast_forward_btn@@" class="btn btn-default" type="button" data-loading-text="..." onclick="feed_history(@@,'fast_forward')" data-toggle="tooltip" data-placement="top" title="all by computer"><span class="glyphicon glyphicon-fast-forward" aria-hidden="true"></span></button>

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

function display_btn(index){
    if (processed_line < index -1){
	processed_line = index - 1;
    }
    for (var i = 1; i < total_line+1; i++){
	$("#bs"+ i.toString()).hide();
	if (i <= processed_line){
	    $("#rs"+ i.toString()).show();
	} else {
	    $("#rs"+ i.toString()).hide();
	}
    }
    $("#bs"+ (processed_line+1).toString()).show();
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

    id = Math.round(Math.random()*1000) + 1
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
	    nline:total_line
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
	    discourage_weight:-5,
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
	}
    }).always(function (){
	btn.button('reset');
	clearInterval(timer);
    });

}
