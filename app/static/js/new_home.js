
var all_data;

getTasks('karate_type')
$('#karate_type').addClass("active");

$(".btn").click(function(){
  $(".btn").removeClass("active");
  $(this).addClass("active");
  getTasks($(this).attr("id"))
});

$(".content").on("click", 'div.new_award', function(){

	var title_text = $(this).children().first().text();
	var title = document.createTextNode(title_text);
	var container;
	for(var i = 1; i < parseInt(all_data[0]); i++){
		if(title_text == all_data[i]['title']){
			container = all_data[i]['container'].split('/');
		}
	}
	var award_detail = document.createElement('div');
	award_detail.className = 'award_detail_container';
	var close = document.createElement('div');
	var close_sign = document.createTextNode('×');
	close.className = 'closeDiv';
	close.appendChild(close_sign);

	var h4 = document.createElement('H4');
	var btn = document.createElement('button');
	var div_btn = document.createElement('div');
	var ul = document.createElement('ul')
	ul.className = 'list-group'
	div_btn.className = 'div_btn';
	btn.innerHTML = 'получить';
	btn.className = 'btn_getAward';
	div_btn.appendChild(btn);

	h4.appendChild(title);
	for(var q = 0; q < container.length; q++){
		if(container[q] != ''){
			var p = document.createElement("p");
			p.appendChild(document.createTextNode(container[q]));
			var li = document.createElement('li');
			li.className = 'list-group-item font'
			li.appendChild(p);
			ul.appendChild(li);
		}
	}

	var div = document.createElement('DIV');
	div.className = 'award_detail';  
	div.appendChild(h4);
	div.appendChild(ul);
	div.appendChild(div_btn);

	award_detail.append(div); 
	award_detail.appendChild(close);

	$('.outPopUp').append(award_detail);
	$('body').append('<span class="mask"></span>');
});


$(".outPopUp").on("click", "div.closeDiv", function(){
    $('.award_detail_container').remove();
    $('.mask').remove();
});

function getTasks(type){
	$.post('/tasksSpecified', {
		type: type
	}).done(function(resp){
		$('.awards_block').remove();
		var awards_block = document.createElement('div');
		awards_block.className = 'awards_block';
		all_data = resp;
		for(var i = 1; i < parseInt(resp[0]); i++){
			var title = document.createTextNode(resp[i]['title']);
			var h4 = document.createElement('H4');
			var btn = document.createElement('button');
			var div_btn = document.createElement('div');
			var ul = document.createElement('ul')
			ul.className = 'list-group'
			div_btn.className = 'div_btn';
			btn.innerHTML = 'получить';
			btn.className = 'btn_getAward';
			div_btn.appendChild(btn);			
			h4.appendChild(title);
			var div = document.createElement('DIV');
			div.className = 'new_award';  
			div.appendChild(h4);
			div.appendChild(ul);
			div.appendChild(div_btn);
			awards_block.appendChild(div); 
		}
		$('.content').prepend(awards_block); 

	}).fail(function(){
		alert('something went wrong')
	});
}
