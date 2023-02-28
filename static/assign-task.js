let fileList = [];
let file_cnt = 0;

function update_form_field_details() {
	const dataTransfer = new DataTransfer()
	for(var i=0; i<fileList.length; i++){
		dataTransfer.items.add(fileList[i]);
	}
	document.getElementById('form_field').files = dataTransfer.files;
	update_dom();
}

function update_dom() {
	let html = document.getElementById('uploaded_file_list').innerHTML;
	if(fileList.length == 0){
		document.getElementById('uploaded_file_list').innerHTML = "";
	}
	else{
		html = "<h2 class='mb-2'>Files Selected</h2> <ul class='file_list p-0'> <hr class='my-2'>";
		for(var i=0; i<fileList.length; i++){
			html = html + "<li class='row align-items-center' id='f-" + file_cnt + "'> <p class='col-10 m-0'>" + fileList[i].name + "</p> <img src='/static/trash_icon.png' class='col-2 trash_icon' onclick='delete_file(this)'></li><hr class='my-2'>";
			file_cnt++;
		}
		document.getElementById('uploaded_file_list').innerHTML = html;
	}
}

function update_file_list() {
	let lst = document.getElementById('form_field').files;
	for(var i=0; i<lst.length; i++){
		fileList.push(lst[i]);
	}
	update_form_field_details();
}


function delete_file(ele) {
	let id = ele.parentNode.id;
	let filename = document.getElementById(id).getElementsByTagName('p')[0].innerHTML;

	for(var i=0; i<fileList.length; i++){
		if(fileList[i].name == filename){
			fileList.splice(i, 1);
			break;
		}
	}
	update_form_field_details();
}

update_dom();