function showValue(newValue,spanID){
			document.getElementById(spanID).innerHTML=newValue;
		}
$('#shake').click(function(){
	var scheme = "";
	$('#nlines').val(14);
	for(var i=1; i<15;i++){
		scheme += "<select id=\"ry" + i + "\" onchange='changeRadio()'><option value='A'";
		if(i===1 || i===3){
			scheme += "selected";
		}
		scheme += ">A</option><option value='B'";
		if(i===2 || i===4){
			scheme += "selected";
		}
		scheme += ">B</option><option value='C'";
		if(i===5 || i===7){
			scheme += "selected";
		}
		scheme += ">C</option><option value='D'";
		if(i===6 || i===8){
			scheme += "selected";
		}
		scheme += ">D</option><option value='E'";
		if(i===9 || i===11){
			scheme += "selected";
		}
		scheme += ">E</option><option value='F'";
		if(i===10 || i===12){
			scheme += "selected";
		}
		scheme += ">F</option><option value='G'";
		if(i===13 || i===14){
			scheme += "selected";
					}
		scheme += ">G</option>";
		scheme += "</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<select id=\"syl" + i + "\" onchange='changeRadio()'><option value='5'>5</option><option value='6'>6</option><option value='7'>7</option><option value='8'>8</option><option value='9'>9</option><option value='10' selected>10</option>" + 
				"</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id=\"rhymeWords" + i +"\" type='text'/><br/>";	
		} 
	$('#rscheme').html(scheme);
		});

$('#petr').click(function(){
	var scheme = "";
	$('#nlines').val(14);
	for(var i=1; i<15;i++){
		scheme += "<select id=\"ry" + i + "\" onchange='changeRadio()'><option value='A'";
		if(i===1 || i===4 || i===5 || i===8){
			scheme += "selected";
		}
		scheme += ">A</option><option value='B'";
		if(i===2 || i===3 || i===6 || i===7){
			scheme += "selected";
		}
		scheme += ">B</option><option value='C'";
		if(i===9 || i===12){
			scheme += "selected";
		}
		scheme += ">C</option><option value='D'";
		if(i===10 || i===13){
			scheme += "selected";
		}
		scheme += ">D</option><option value='E'";
		if(i===11 || i===14){
			scheme += "selected";
		}
		scheme += ">E</option><option value='F'>F</option><option value='G'>G</option>";
		scheme += "</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<select id=\"syl" + i + "\" onchange='changeRadio()'><option value='5'>5</option><option value='6'>6</option><option value='7'>7</option><option value='8'>8</option><option value='9'>9</option><option value='10' selected>10</option>" + 
				"</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id=\"rhymeWords" + i +"\" type='text'/><br/>";	
	} 
	$('#rscheme').html(scheme);
});

$('#haiku').click(function(){
	var scheme = "";
	$('#nlines').val(3);
	for(var i=1; i<4;i++){
		scheme += "<select id=\"ry" + i + "\" onchange='changeRadio()'><option value='A'";
		if(i===1){
			scheme += "selected";
		}
		scheme += ">A</option><option value='B'";
		if(i===2){
			scheme += "selected";
		}
		scheme += ">B</option><option value='C'";
		if(i===3){
			scheme += "selected";
		}
		scheme += ">C</option><option value='D'>D</option><option value='E'>E</option><option value='F'>F</option><option value='G'>G</option>";
		scheme += "</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<select id=\"syl" + i + "\" onchange='changeRadio()'><option value='5'";
		if(i===1 || i===3){
			scheme += "selected";
		}
		scheme += ">5</option><option value='6'>6</option><option value='7'";
		if(i===2){
			scheme += "selected";
		}
		scheme += ">7</option><option value='8'>8</option><option value='9'>9</option><option value='10'>10</option>" + 
				"</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id=\"rhymeWords" + i +"\" type='text'/><br/>";	
	} 
	$('#rscheme').html(scheme);

});

$(document).ready(function(){
	var scheme = "";
	$('#nlines').val(2);
	for(var i=1; i<3; i++){
		scheme += "<select id=\"ry" + i + "\" onchange='changeRadio()'><option value='A' selected>A</option><option value='B'>B</option><option value='C'>C</option><option value='D'>D</option><option value='E'>E</option><option value='F'>F</option><option value='G'>G</option></select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<select id=\"syl" + i + "\" onchange='changeRadio()'><option value='5'>5</option><option value='6'>6</option><option value='7'>7</option><option value='8' selected>8</option><option value='9'>9</option><option value='10'>10</option></select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id=\"rhymeWords" + i + "\" type='text'/><br/>";
	}
	$('#rscheme').html(scheme);
});

$('#coup').click(function(){
	var scheme = "";
	$('#nlines').val(2);
	for(var i=1; i<3; i++){
		scheme += "<select id=\"ry" + i + "\" onchange='changeRadio()'><option value='A' selected>A</option><option value='B'>B</option><option value='C'>C</option><option value='D'>D</option><option value='E'>E</option><option value='F'>F</option><option value='G'>G</option></select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<select id=\"syl" + i + "\" onchange='changeRadio()'><option value='5'>5</option><option value='6'>6</option><option value='7'>7</option><option value='8' selected>8</option><option value='9'>9</option><option value='10'>10</option></select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id=\"rhymeWords" + i + "\" type='text'/><br/>";
		}
	$('#rscheme').html(scheme);
});

function changeRadio(){
	$('#usr').prop("checked",true);
}

$('#rndm').click(function(){

	var choice = Math.floor((Math.random()*6)+1);
	switch(choice){
		case 1:
			var scheme = "";
			$('#nlines').val(14);
			for(var i=1; i<15;i++){
				scheme += "<select id=\"ry" + i + "\" onchange='changeRadio()'><option value='A'";
				if(i===1 || i===2){
					scheme += "selected";
				}
				scheme += ">A</option><option value='B'";
				if(i===3 || i===4){
					scheme += "selected";
				}
				scheme += ">B</option><option value='C'";
				if(i===5 || i===6){
					scheme += "selected";
				}
				scheme += ">C</option><option value='D'";
				if(i===7 || i===8){
					scheme += "selected";
				}
				scheme += ">D</option><option value='E'";
				if(i===9 || i===10){
					scheme += "selected";
				}
				scheme += ">E</option><option value='F'";
				if(i===11 || i===12){
					scheme += "selected";
				}
				scheme += ">F</option><option value='G'";
				if(i===13 || i===14){
					scheme += "selected";
				}
				scheme += ">G</option>";
				scheme += "</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<select id=\"syl" + i + "\" onchange='changeRadio()'><option value='5'>5</option><option value='6'>6</option><option value='7'>7</option><option value='8'>8</option><option value='9'>9</option><option value='10' selected>10</option>" + 
						"</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id=\"rhymeWords" + i +"\" type='text'/><br/>";	
			} 
			$('#rscheme').html(scheme);
			break;

		case 2:
			var scheme = "";
			$('#nlines').val(14);
				for(var i=1; i<15;i++){
					scheme += "<select id=\"ry" + i + "\" onchange='changeRadio()'><option value='A'";
					if(i===1 || i===2 || i===5 || i===6 || i===9 || i===10 || i===13 || i===14){
						scheme += "selected";
					}
					scheme += ">A</option><option value='B'";
					if(i===3 || i===4 || i===7 || i===8 || i===11 || i===12){
						scheme += "selected";
					}
					scheme += ">B</option><option value='C'>C</option><option value='D'>D</option><option value='E'>E</option><option value='F'>F</option><option value='G'>G</option>";
					scheme += "</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<select id=\"syl" + i + "\" onchange='changeRadio()'><option value='5'>5</option><option value='6'>6</option><option value='7'>7</option><option value='8'>8</option><option value='9'>9</option><option value='10' selected>10</option>" + 
							"</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id=\"rhymeWords" + i +"\" type='text'/><br/>";	
				} 
				$('#rscheme').html(scheme);
				break;

		case 3:
			var scheme = "";
			$('#nlines').val(14);
			for(var i=1; i<15;i++){
				scheme += "<select id=\"ry" + i + "\" onchange='changeRadio()'><option value='A'";
				if(i===1 || i===4){
					scheme += "selected";
				}
				scheme += ">A</option><option value='B'";
				if(i===2 || i===5){
					scheme += "selected";
				}
				scheme += ">B</option><option value='C'";
				if(i===3 || i===6){
					scheme += "selected";
				}
				scheme += ">C</option><option value='D'";
				if(i===7 || i===9){
					scheme += "selected";
				}
				scheme += ">D</option><option value='E'";
				if(i===8 || i===10){
					scheme += "selected";
				}
				scheme += ">E</option><option value='F'";
				if(i===11 || i===13){
					scheme += "selected";
				}
				scheme += ">F</option><option value='G'";
				if(i===12 || i===14){
					scheme += "selected";
				}
				scheme += ">G</option>";
				scheme += "</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<select id=\"syl" + i + "\" onchange='changeRadio()'><option value='5'>5</option><option value='6'>6</option><option value='7'>7</option><option value='8'>8</option><option value='9'>9</option><option value='10' selected>10</option>" + 
						"</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id=\"rhymeWords" + i +"\" type='text'/><br/>";	
			} 
			$('#rscheme').html(scheme);
			break;

		case 4:
			var scheme = "";
			$('#nlines').val(3);
			for(var i=1; i<4;i++){
				scheme += "<select id=\"ry" + i + "\" onchange='changeRadio()'><option value='A'";
				if(i===1 || i===3){
					scheme += "selected";
				}
				scheme += ">A</option><option value='B'";
				if(i===2){
					scheme += "selected";
				}
				scheme += ">B</option><option value='C'>C</option><option value='D'>D</option><option value='E'>E</option><option value='F'>F</option><option value='G'>G</option>";
				scheme += "</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<select id=\"syl" + i + "\" onchange='changeRadio()'><option value='5'";
				if(i===1 || i===3){
					scheme += "selected";
				}
				scheme += ">5</option><option value='6'>6</option><option value='7'";
				if(i===2){
					scheme += "selected";
				}
				scheme += ">7</option><option value='8'>8</option><option value='9'>9</option><option value='10'>10</option>" + 
						"</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id=\"rhymeWords" + i +"\" type='text'/><br/>";	
			} 
			$('#rscheme').html(scheme);
			break;

		case 5:
			var scheme = "";
			$('#nlines').val(3);
			for(var i=1; i<4;i++){
				scheme += "<select id=\"ry" + i + "\" onchange='changeRadio()'><option value='A'";
				if(i===1 || i===2){
					scheme += "selected";
				}
				scheme += ">A</option><option value='B'";
				if(i===3){
					scheme += "selected";
				}
				scheme += ">B</option><option value='C'>C</option><option value='D'>D</option><option value='E'>E</option><option value='F'>F</option><option value='G'>G</option>";
				scheme += "</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<select id=\"syl" + i + "\" onchange='changeRadio()'><option value='5'";
				if(i===1 || i===3){
					scheme += "selected";
				}
				scheme += ">5</option><option value='6'>6</option><option value='7'";
				if(i===2){
					scheme += "selected";
				}
				scheme += ">7</option><option value='8'>8</option><option value='9'>9</option><option value='10'>10</option>" + 
						"</select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id=\"rhymeWords" + i +"\" type='text'/><br/>";	
			} 
			$('#rscheme').html(scheme);
			break;

		case 6:
			var scheme = "";
			$('#nlines').val(2);
			for(var i=1; i<3; i++){
					scheme += "<select id=\"ry" + i + "\" onchange='changeRadio()'><option value='A' selected>A</option><option value='B'>B</option><option value='C'>C</option><option value='D'>D</option><option value='E'>E</option><option value='F'>F</option><option value='G'>G</option></select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<select id=\"syl" + i + "\" onchange='changeRadio()'><option value='5'>5</option><option value='6'>6</option><option value='7'>7</option><option value='8'>8</option><option value='9'>9</option><option value='10' selected>10</option></select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id=\"rhymeWords" + i + "\" type='text'/><br/>";
				}
			$('#rscheme').html(scheme);	
	}
});

$('#translate-button').click(function(){
	var n = parseInt($('#nlines').val());
	var config = {};
	var rs = [];
	var syl = [];
	var wrds = [];
	for(var i=0;i<n;i++){
		rs[i] = $('#ry'+(i+1)).val();
		syl[i] = parseInt($('#syl'+(i+1)).val());
		wrds[i] = $('#rhymeWords'+(i+1)).val();
	}
	config['Nlines'] = $('#nlines').val()
	config['RhymeScheme'] = rs;
	config['Syllables'] = syl;
	config['RhymeWords'] = wrds;
	config['CurseWords'] = parseInt($('#cwords').val());
	config['Repetitions'] = parseInt($('#reps').val());
	config['Alliteration'] = parseInt($('#allit').val());
	config['SlantRhyme'] = parseInt($('#slant').val());
	config['WordLen'] = parseInt($('#wordlen').val());
	config['Author'] = $("input[name='author']:checked").val()
	config['Encourage'] = $('#ewords').val()
	config['Discourage'] = $('#dwords').val()
	config['StartPhrase'] = $('#startwords').val()
	config['Lang'] = $("input[name='lang']:checked").val()
	config['Genre'] = $("input[name='genre']:checked").val()
	config['Meter'] = $("input[name='meter']:checked").val()

	//$('#conf').html(JSON.stringify(config));
});
		
function RS(val){
	var scheme = "";
	var value = parseInt(val);
	for(var i=1; i<=value; i++){
		scheme += "<select id=\"ry" + i + "\"><option value='A'>A</option><option value='B'>B</option><option value='C'>C</option><option value='D'>D</option><option value='E'>E</option><option value='F'>F</option><option value='G'>G</option></select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<select id=\"syl" + i + "\"><option value='5'>5</option><option value='6'>6</option><option value='7'>7</option><option value='8'>8</option><option value='9'>9</option><option value='10'>10</option></select>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input id=\"rhymeWords" + i + "\" type='text'/><br/>";
	}
	$("#rscheme").html(scheme);
	changeRadio();
}

$('#cwords').slider({
	formatter: function(value) {
		return 'Current value: ' + value;
	}
});

$('#reps').slider({
	formatter: function(value) {
		return 'Current value: ' + value;
	}
});

$('#allit').slider({
	formatter: function(value) {
		return 'Current value: ' + value;
	}
});

$('#slant').slider({
	formatter: function(value) {
		return 'Current value: ' + value;
	}
});

$('#wordlen').slider({
	formatter: function(value) {
		return 'Current value: ' + value;
	}
});