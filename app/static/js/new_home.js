
getTasks('karate_type')
$('#karate_type').addClass("active");

$(".btn").click(function(){
  $(".btn").removeClass("active");
  $(this).addClass("active");
  getTasks($(this).attr("id"))
})

function getTasks(type){
	$.post('/tasksSpecified', {
		type: type
	}).done(function(resp){
		$('.awards_block').remove();
		var awards_block = document.createElement('div');
		awards_block.className = 'awards_block';
		for(var i = 1; i < parseInt(resp[0]); i++){
			var title = document.createTextNode(resp[i]['title']);
			var container = document.createTextNode(resp[i]['container']);
			var p = document.createElement("p");  
			var h4 = document.createElement('H4');
			h4.appendChild(title);
			p.appendChild(container);

			var div = document.createElement('DIV');
			div.className = 'new_award';  
			div.appendChild(h4);
			div.appendChild(p);
			awards_block.appendChild(div); 
		}
		$('.content').prepend(awards_block); 

	}).fail(function(){
		alert('something went wrong')
	});
}
