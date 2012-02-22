$(document).ready(function(){
	if($('#id_subscribe_type').attr('value') == 'content'){
		$('#id_content_type').change(function(){
			var message = $('#id_message');
			var hidden = $('#id_hidden_message');
			var tmp_src = message.val();
			var new_text_src = hidden.val();
			message.text(new_text_src);
			var instance = mirrorInstances[message[0]];
			instance.setValue(new_text_src);
			instance.refresh();
			hidden.text(tmp_src);
		})
	}
	if($('#id_subscribe_type').attr('value') == 'sometime'){
		var setup = false;
		if($('#id_content_type').val() == 'html'){
			setupTINYMCE('id_message');
			tinyMCE.execCommand('mceToggleEditor',false,'id_message');
			setup = true;
		}
		$('#id_content_type').change(function(){
			if($(this).val() == 'html'){
				if(!setup){
					setupTINYMCE('id_message');
					setup = true;
				}
			}
			tinyMCE.execCommand('mceToggleEditor',false,'id_message');
			if($(this).val() == 'plain'){
				var val = tinyMCE.get('id_message').getContent({format : 'raw'});
				var tmp = document.createElement("DIV");
			    tmp.innerHTML = val;
				$('#id_message').val(tmp.textContent);
			}
		})
	}
});

