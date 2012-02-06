
$(document).ready(function(){
	$("#id_subscribe_type option:selected").each(function (i,item) {
           if($(item).attr('value') == 'sometime'){
			$('.sometime_subscribe').show();
			$('.content_subscribe').hide();
		}else{
			$('.sometime_subscribe').hide();
			$('.content_subscribe').show();
		}
       });
	$('#id_subscribe_type').change(function(){
		$("#id_subscribe_type option:selected").each(function (i,item) {
            if($(item).attr('value') == 'sometime'){
				$('.sometime_subscribe').show();
				$('.content_subscribe').hide();
			}else{
				$('.sometime_subscribe').hide();
				$('.content_subscribe').show();
			}
        });
	})
});