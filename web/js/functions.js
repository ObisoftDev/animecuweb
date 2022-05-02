function appendEpisodie(name,imgurl,epiurl,id=0){
	html = '<a href="'+epiurl+'" id="epi-'+id+'">'
	html+= '<div class="anime-item" ><img ';
	html+= 'src="'+imgurl+'">'
	html+= '<h3>'+name+'</h3>';
	html+= '</div>';
	html+= '</a>'
	$('#center-content').append(html)
}