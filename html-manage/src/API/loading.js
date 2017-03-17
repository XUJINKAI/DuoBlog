export var loading = (function(){
	var event_done = []; //['event1', 'event2']
	var callback_list = []; //[[callback1, ['event1']], [callback2, ['event2', 'event3']]]

	function arrayContainsAnotherArray(needle, haystack){
		for(var i = 0; i < needle.length; i++){
		if(haystack.indexOf(needle[i]) === -1)
			return false;
		}
		return true;
	}
	
	return {
		run_after: function(callback, event){
			if(typeof(event)=='string') {
				event = [event];
			}
			if(arrayContainsAnotherArray(event, event_done)) {
				callback();
			} else {
				callback_list.push([callback, event]);
			}
		},
		done: function(event){
			if( ! event_done.includes(event)) {
				event_done.push(event);
			}
			for (var i = callback_list.length - 1; i >= 0; i--) {
				var item = callback_list[i];
				var events = item[1];
				var all_done = true;
				events.forEach(function(event){
					if( ! event_done.includes(event)) {
						all_done = false;
					}
				})
				if(all_done) {
					var callback = item[0];
					callback();
					callback_list.splice(i ,1);
				}
			}
		},
		undo: function(event){
			if(event_done.includes(event)) {
				event_done.splice(event_done.indexOf(event), 1);
			}
		},
	}
})();