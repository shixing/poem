

$('#enc').slider().on('change',function(event){
    a = [0,1,2,3,4,5,6];
    $("input[name=enc_weight]").val(a[event.value.newValue + 3]);
});

$("input[name=enc_weight]").val(1);

$('#cwords').slider().on('change',function(event){
    a = [-5,0,4,5]
    $("input[name=cword_weight]").val(a[event.value.newValue]);
});


$('#reps').slider().on('change',function(event){
    a = [0,2.5,3,3.5]
    $("input[name=reps_weight]").val(a[event.value.newValue]);
});

$('#allit').slider().on('change',function(event){
    a = [-3.0,-2.0,-1.0,0.0,1.0,2.0,3.0];
    $("input[name=allit_weight]").val(a[event.value.newValue + 3]);
});

$('#slant').slider().on('change',function(event){
    a = [-3.0,-2.0,-1.0,0.0,1.0,2.0,3.0];
    $("input[name=slant_weight]").val(a[event.value.newValue + 3]);
});

$('#wordlen').slider().on('change',function(event){
    a = [-0.06,-0.03,-0.01,0.0,0.01,0.03,0.06];
    $("input[name=wordlen_weight]").val(a[event.value.newValue + 3]);
});
