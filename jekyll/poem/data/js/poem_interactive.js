var guidelines = ["Let Hafez recommend some rhyme words first","Please confirm the rhyme words by clicking \"Confirm\"","Rhyme words and beam size are confirmed. Let's start !"]

//global id;
var gid = 0;
var total_line = 14;
nline_onchange(14);

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
    <div id="bs@@" style="display:none">
      <div class="col-lg-1">
	<button id="forward_btn1" class="btn btn-default" type="button" data-loading-text="..." onclick="forward(@@)" data-toggle="tooltip" data-placement="top" title="Generate this line by Computer"><span class="glyphicon glyphicon-play" aria-hidden="true"></span></button>
      </div>
      <div class="col-lg-1">
	<button id="fast_forward_btn1" class="btn btn-default" type="button" data-loading-text="..." onclick="fast_forward(@@)" data-toggle="tooltip" data-placement="top" title="Generate all the rest lines by Computer"><span class="glyphicon glyphicon-fast-forward" aria-hidden="true"></span></button>
      </div>
      <div class="col-lg-1">
	<button id="upload_btn1" class="btn btn-default" type="button" data-loading-text="..." onclick="upload(@@)" data-toggle="tooltip" data-placement="top" title="Let human write this line and submit to server"><span class="glyphicon glyphicon-cloud-upload" aria-hidden="true"></span></button>
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
    for (var i = 1; i < total_line+1; i++){
	$("#bs"+ i.toString()).hide();
    }
    $("#bs"+ index.toString()).show();
}

function disable_model(disable){
    //$('input[name=model]').attr("disabled",disable);
}

function clear_line_rhyme(){
    for (var i = 1; i < total_line+1; i++){
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
    for (var i = 1; i < total_line+1; i++){
	word = $("#rhyme"+ i.toString()).val();
	words.push(word);
    }
    words_str = JSON.stringify(words)


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
	url: "http://cage.isi.edu:8080/api/confirm",
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
	url: "http://cage.isi.edu:8080/api/rhyme",
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
	}
    }).always(function (){
	btn.button('reset');
	clearInterval(timer);
    });

}

function forward(index){
    var btn = $("#forward_btn"+index.toString());
    btn.button('loading');

    //model = $("input[name=model]:checked").val();
    model = 0;
    action = "fsaline";

    id = gid;
    
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
	url: "http://cage.isi.edu:8080/api/poem_interactive",
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

    //model = $("input[name=model]:checked").val();
    model = 0;
    action = "fsa";

    id = gid;
    
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
	url: "http://cage.isi.edu:8080/api/poem_interactive",
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

    //model = $("input[name=model]:checked").val();
    model = 0;
    action = "words";

    id = gid;
    words = $("#line"+index.toString()).val();
    
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
    },2000);

    $.ajax({
	url: "http://cage.isi.edu:8080/api/poem_interactive",
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
