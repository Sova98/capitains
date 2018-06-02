
//onstart
setActivebtn("karate");

function setActivebtn(id){
	var btns = document.getElementsByClassName("optionListBtn");

	for(var i = 0; i < btns.length; i++){
		btns[i].setAttribute( 'style', 'background-color: #eae8e2!important;');
	}

	document.getElementById(id).setAttribute( 'style', 'background-color: #F9F8F3!important;');
	getTasks(id)
}
function getTasks(type){
	$.post('/tasksSpecified', {
		type: type
	}).done(function(resp){
		var divCont = document.getElementsByClassName('nav flex-column')[1];
		while (divCont.firstChild) {
		  divCont.removeChild(divCont.firstChild);
		}
		for(var i = 1; i < parseInt(resp[0])+1; i++){
			var textnode = document.createTextNode(resp[i]['title']);
			var node = document.createElement("LI");  
			node.className = 'nav-item';
			var h3 = document.createElement('H3');
			h3.appendChild(textnode);
			var div = document.createElement('DIV');
			div.className = 'task';  
			div.appendChild(h3);
			node.appendChild(div);
			divCont.appendChild(node);  
		}

	}).fail(function(){
		alert('something went wrong')
	});
}
/*			{% for t in tasks %}
			  <li class="nav-item">
			    <div class="task">
			    	<h3>{{t.title}}</h3>
			    	<hr />
			    	<p>{{t.container}}</p>
			    	<div class="row">
						<div class="col-sm-6" style="text-align: left;">
							<button type="button" class="btn btn-success">ВЫПОЛНИЛ</button>
						</div>

						<div class="col-sm-6" style="text-align: right;">
							<span>уже выполнили 15 чел</span>
					</div>
			    </div>
			  </li>
		  	{% endfor %}*/