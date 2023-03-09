if(profileUser != loggedInUser){
    document.getElementById("change_password_block").style.display = "none";
}

function checkPassword() {
    let old_password = document.getElementById('old_password').value;
    let new_password = document.getElementById('new_password').value;
    let confirm_new_password = document.getElementById('confirm_new_password').value;
    if(old_password=='' && new_password=='' && confirm_new_password==''){
        document.getElementById('password_rules').style.display = "none";
        document.getElementById('submit_button').disabled = false;
    }
    else if(new_password == confirm_new_password && new_password != '' && old_password != ''){
        //check for correct password
        let hasNumber = false, hasUpperCase = false;
        for(let i=0; i<new_password.length; i++){
            if(new_password[i]>='0' && new_password[i]<='9'){
                hasNumber = true;
            }
            else if(new_password[i]>='A' && new_password[i]<='Z'){
                hasUpperCase = true;
            }
        }

        // hide the rule section amd enable the submit button
        if(new_password.length>=8 && hasUpperCase==true && hasNumber==true){
            document.getElementById('submit_button').disabled = false;
            document.getElementById('password_rules').style.display = "none";
        }
        else{
            document.getElementById('submit_button').disabled = true;
        }

    }
    else{
        document.getElementById('password_rules').style.display = "block";
        document.getElementById('submit_button').disabled = true;
    }
}