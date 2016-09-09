

$('#enc').slider().on('slide',function(event){
    a = [0,1,2,3,4,5,6];
    $("input[name=enc_weight]").val(a[event.value + 3]);
});

$("input[name=enc_weight]").val(1);

$('#cwords').slider().on('slide',function(event){
    a = [-3.0,-2.0,-1.0,0.0,1.0,2.0,3.0];
    $("input[name=cword_weight]").val(a[event.value + 3]);
});


$('#reps').slider().on('slide',function(event){
    a = [-3.0,-2.0,-1.0,0.0,1.0,2.0,3.0];
    $("input[name=reps_weight]").val(a[event.value + 3]);
});

$('#allit').slider().on('slide',function(event){
    a = [-3.0,-2.0,-1.0,0.0,1.0,2.0,3.0];
    $("input[name=allit_weight]").val(a[event.value + 3]);
});

$('#slant').slider().on('slide',function(event){
    a = [-3.0,-2.0,-1.0,0.0,1.0,2.0,3.0];
    $("input[name=slant_weight]").val(a[event.value + 3]);
});

$('#wordlen').slider().on('slide',function(event){
    a = [-0.06,-0.03,-0.01,0.0,0.01,0.03,0.06];
    $("input[name=wordlen_weight]").val(a[event.value + 3]);
});
