document.querySelector("#login-click").addEventListener('click', () => {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    console.log(email,password);
    $.ajax({
        type: 'POST',
        url: '/',
        data: {
            'email': email,
            'password': password,
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
        },
        success: (response) => {
            if (response.success) {
                alert(response.message);
                window.location.href = response.url_pattern;
            } else {
                alert(response.message);
            }
        },
    });
});


document.getElementById("registration-create").addEventListener('click', () => {
    let email = document.getElementById("email").value;
    // let check = email in endswith("@gmail.com");
    // console.log(check)
    // if(!check){
    //     alert("invalid email-ID")
    //     return;
    // }
    let password = document.getElementById("password").value;
    let repassword = document.getElementById("repassword").value;
    console.log(email, password, repassword);
    if (password != repassword) {
        alert("Please check your password");
        return;
    }
    $.ajax({
        type: "POST",
        url: '/register/',
        data: {
            'email': email,
            'password': password,
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
        },
        success: (response) => {
            if (response.success) {
                alert(response.message);
                window.location.href = response.url_pattern;
            }
        },
    });
});
