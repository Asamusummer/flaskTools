$(".nowpage").keyup(function(e) {
	$(this).change();
	if(e.keyCode==13){
		torefreshclick();
	}
});
$(".nowpage").change(function(e){
	changeInput(this);
})
$("input[type='nunber']").keyup(function(e) {
	$(this).change();
});
$("input[type='nunber']").change(function(e){
	changeInput(this);
})
function changeInput(bt){
	bt.value=bt.value.replace(/\D/g,'');
	count=Number($(bt).val());
	if(count<Number($(bt).attr("min"))){
		count=Number($(bt).attr("min"));
	}
	if(count>Number($(bt).attr("max"))){
		count=Number($(bt).attr("max"));
	}
	$(bt).val(count);
}
