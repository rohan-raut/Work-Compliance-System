function add_new_row() {
    let html = document.getElementById('hierarchy_table').tBodies[0].innerHTML;
    // html = html + '<tr id="row_number_' + cnt_rows + '"><td><input type="text" name="user_role_' + cnt_rows + '"></td><td><input type="number" name="priority_' + cnt_rows + '"></td><td><input type="checkbox" name="show_report_' + cnt_rows + '"></td><td><button type="button" class="btn btn-sm btn-danger delete_btn" onclick="delete_row(\'row_number_' + cnt_rows + '\')">Delete</button></td></tr>';
    html = html + '<tr id="row_number_' + cnt_rows + '"><td><input id="user_role_' + cnt_rows + '" type="text" name="user_role_' + cnt_rows + '" onchange="changeValInput(\'user_role_' + cnt_rows + '\')"></td><td><input id="priority_' + cnt_rows + '" type="number" name="priority_' + cnt_rows + '" onchange="changeValInput(\'priority_' + cnt_rows + '\')"></td><td><input id="show_report_' + cnt_rows + '" type="text" value="N" name="show_report_' + cnt_rows + '" onchange="changeValInput(\'show_report_' + cnt_rows + '\')"></td><td><button type="button" class="btn btn-sm btn-danger delete_btn" onclick="delete_row(\'row_number_' + cnt_rows + '\')">Delete</button></td></tr>'
    document.getElementById('hierarchy_table').tBodies[0].innerHTML = html;
    cnt_rows = cnt_rows + 1;
}

function delete_row(EleId) {
    let ele = document.getElementById(EleId);
    ele.remove();
}


function changeValInput(InpID) {
    let ele = document.getElementById(InpID);
    let val = ele.value;
    ele.setAttribute('value', val);
}




// call the api in frontend, no other option 
