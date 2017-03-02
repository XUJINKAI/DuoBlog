function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
					var cookie = jQuery.trim(cookies[i]);
					// Does this cookie string begin with the name we want?
					if (cookie.substring(0, name.length + 1) === (name + '=')) {
							cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
							break;
					}
			}
	}
	return cookieValue;
}
function log(msg) {
	if(typeof(DEBUG)=='boolean'&&DEBUG){
		console.log(msg);
	}
}

//ajax
function ajax_data(method, url, data, success, error, complete) {
	if(!method || !url) return;
	log(method + ': ' + url + ', {parameter}↓↓↓');
	log(data)
	return $.ajax({
		url: url,
		method: method,
		headers: {
			'X-CSRFToken': getCookie('csrftoken'),
		},
		dataType: 'json',
		data: data,
		success: function(data) {
			if(success) { success(data); }
		},
		error: function(data) {
			log(data.responseText);
			if(error) { error(data); }
		},
		complete: function(data) {
			if(complete) { complete(data); }
		},
	})
}
function get_data(url, data, success, error, complete) {
	return ajax_data('GET', url, data, success, error, complete)
}
function post_data(url, data, success, error, complete) {
	return ajax_data('POST', url, data, success, error, complete);
}
function put_data(url, data, success, error, complete) {
	return ajax_data('PUT', url, data, success, error, complete);
}
function patch_data(url, data, success, error, complete) {
	return ajax_data('PATCH', url, data, success, error, complete);
}
function delete_data(url, data, success, error, complete) {
	return ajax_data('DELETE', url, data, success, error, complete);
}

// Array
Array.prototype.remove = function() {
	var what, a = arguments, L = a.length, ax;
	while (L && this.length) {
		what = a[--L];
		while ((ax = this.indexOf(what)) !== -1) {
			this.splice(ax, 1);
		}
	}
	return this;
};
Array.prototype.move = function (old_index, new_index) {
	if(old_index<0 || old_index>=this.length 
		|| new_index<0 || new_index>=this.length){
		return this;
	}
	if (new_index >= this.length) {
		var k = new_index - this.length;
		while ((k--) + 1) {
			this.push(undefined);
		}
	}
	this.splice(new_index, 0, this.splice(old_index, 1)[0]);
	return this; // for testing purposes
};