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


