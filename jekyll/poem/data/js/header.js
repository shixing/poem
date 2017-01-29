api_host = "vivaldi.isi.edu"

function update_npoem(){
    $.ajax({
	url: "http://"+api_host+":8080/api/npoem",
	data : {},
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
	    $("#npoem").html(jd.value);
	}
    }).always(function (){
    });

}

update_npoem();
