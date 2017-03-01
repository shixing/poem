function range(start, end, step, offset) {
  
  var len = (Math.abs(end - start) + ((offset || 0) * 2)) / (step || 1) + 1;
  var direction = start < end ? 1 : -1;
  var startingPoint = start - (direction * (offset || 0));
  var stepSize = direction * (step || 1);
  
  return Array(len).fill(0).map(function(_, index) {
    return startingPoint + (stepSize * index);
  });
  
}


$('#enc').slider().on('change',function(event){
    a = range(0,5,0.1)
    $("input[name=enc_weight]").val(a[event.value.newValue]);
});


$('#cwords').slider().on('change',function(event){
    a = range(-5,5,0.2)
    $("input[name=cword_weight]").val(a[event.value.newValue]);
});



$('#reps').slider().on('change',function(event){
    a = range(-5,5,0.2)
    $("input[name=reps_weight]").val(a[event.value.newValue]);
});


$('#allit').slider().on('change',function(event){
    a = range(0,5,0.1)
    $("input[name=allit_weight]").val(a[event.value.newValue]);
});


$('#wordlen').slider().on('change',function(event){
    a = range(0, 0.1, 0.002)
    $("input[name=wordlen_weight]").val(a[event.value.newValue]);
});


$('#topical').slider().on('change',function(event){
    a = range(0,5,0.1)
    $("input[name=topical_weight]").val(a[event.value.newValue]);
});


$('#mono').slider().on('change',function(event){
    a = range(-5,5,0.2)
    $("input[name=mono_weight]").val(a[event.value.newValue]);
});


$('#sentiment').slider().on('change',function(event){
    a = range(-5,5,0.2)
    $("input[name=sentiment_weight]").val(a[event.value.newValue]);
});


$('#concrete').slider().on('change',function(event){
    a = range(-5,5,0.2)
    $("input[name=concrete_weight]").val(a[event.value.newValue]);
});

function reset_style(){

    $('input[name=encourage_words]').val("");
    $('input[name=disencourage_words]').val("");

    $("input[name=enc_weight]").val(5);

    $("#cwords").slider().slider("setValue",0,true,true);
    $("input[name=cword_weight]").val(-5);

    $("#reps").slider().slider("setValue",25,true,true);
    $("input[name=reps_weight]").val(0);

    $("#allit").slider().slider("setValue",0,true,true);
    $("input[name=allit_weight]").val(0);

    $("#wordlen").slider().slider("setValue",0,true,true);
    $("input[name=wordlen_weight]").val(0);
    
    $("#topical").slider().slider("setValue",10,true,true);
    $("input[name=topical_weight]").val(1.0);

    $("#mono").slider().slider("setValue",0,true,true);
    $("input[name=mono_weight]").val(-5);

    $("#sentiment").slider().slider("setValue",25,true,true);
    $("input[name=sentiment_weight]").val(0);

    $("#concrete").slider().slider("setValue",25,true,true);
    $("input[name=concrete_weight]").val(0);

}

function is_default_setting(){
    default_values = [5,-5,0,0,0,1.0,-5,0,0];
    weight_names = ["enc_weight","cword_weight","reps_weight","allit_weight","wordlen_weight","topical_weight","mono_weight","sentiment_weight","concrete_weight"];
    for (i = 0; i < weight_names.length; i ++){
	val = $("input[name="+weight_names[i]+"]").val();
	console.log(weight_names[i]);
	console.log(val);
	console.log(default_values[i]);
	if (default_values[i] != val){
	    return 0;
	}
    }
    return 1;
}
