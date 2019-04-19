function upload_response(response){
    item_key = document.getElementById("key").innerHTML;
    userid = document.getElementById("userid").innerHTML;
    var now = new Date();
    $.post('/api/response',
	   JSON.stringify({
	       'when': now.toUTCString(),
	       'key_id': item_key,
	       'userid': userid,
	       'value': response}
			 ),
	   update_page(),
	   'application/json')
}


function update_page(){
    $.getJSON("/api/data", function(data){
	document.getElementById("key").innerHTML=data.key;
	document.getElementById("target").src=data.image;
	document.getElementById("text").innerHTML=data.string;
    }
	 )
}

function boot_page(){
    $.getJSON("/api/data", function(data){
	document.getElementById("userid").innerHTML=Math.random().toString(36).substring(7);
	document.getElementById("key").innerHTML=data.key;
	document.getElementById("target").src=data.image;
	document.getElementById("text").innerHTML=data.string;	
    }
	     )
}
