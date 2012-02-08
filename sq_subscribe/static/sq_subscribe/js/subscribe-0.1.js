
$(document).ready(function(){
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
});