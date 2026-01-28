function createUser(){
    const URL = "http://127.0.0.1:8000/user-api/";
    const dashboardUrl = "{% url 'user_dashboard' %}"

    fetch(URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: document.getElementById('usr-username').value,
            first_name: document.getElementById('usr-firstname').value,
            last_name: document.getElementById('usr-lastname').value,
            email: document.getElementById('usr-email').value,
            role: document.getElementById('usr-role').value,
            password: document.getElementById('usr-pass').value
        })
    })
        .then(res => res.json())
        .then(data => {
            if(data.message) {
                alert(data.message);
                document.getElementById('modal').style.display = "none";
            }
        })
        .catch(err => alert(err))

}


function createAdmin(){
    const URL = "http://127.0.0.1:8000/user-api/";
    const dashboardUrl = "{% url 'user_dashboard' %}"

    fetch(URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: document.getElementById('ad-username').value,
            first_name: document.getElementById('ad-firstname').value,
            last_name: document.getElementById('ad-lastname').value,
            email: document.getElementById('ad-email').value,
            role: document.getElementById('ad-role').value,
            password: document.getElementById('ad-pass').value
        })
    })
        .then(res => res.json())
        .then(data => {
            if(data.message) {
                alert(data.message);
                document.getElementById('modal2').style.display = "none";
            }
        })
        .catch(err => alert(err))

}