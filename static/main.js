function refresh(){
    $.getJSON("/api/data", function(data){
	document.getElementById("target").src=data.image;
	document.getElementById("text").innerHTML=data.string;
    }
	 )
}
