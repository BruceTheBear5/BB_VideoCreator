let signin = document.getElementById("signin");
let signup = document.getElementById("signup");
let admin = document.getElementById("Admin");
let normal = document.getElementById("Normal");
let error = document.getElementById("Error");

function toggleForms() {
    if (signin.style.display === "none") {
        signin.style.display = "flex";
        signup.style.display = "none";
    } else {
        signin.style.display = "none";
        signup.style.display = "flex";
        admin.style.display = "none";
        normal.style.display = "none";
        error.style.display = "none";
    }
}

function signIn() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    if (username == "admin" && password == "admin") {
        document.documentElement.style.setProperty('--isAdmin', 'true');
        document.documentElement.style.setProperty('--isLogin', 'false');
        admin.style.display = "flex";
        normal.style.display = "none";
        error.style.display = "none";
    }
    else if (username == "user" && password == "1234") {
        document.documentElement.style.setProperty('--isLogin', 'true');
        document.documentElement.style.setProperty('--isAdmin', 'false');
        normal.style.display = "flex";
        admin.style.display = "none";
        error.style.display = "none";
    }
    else {
        document.documentElement.style.setProperty('--isAdmin', 'false');
        document.documentElement.style.setProperty('--isLogin', 'false');
        error.style.display = "flex";
        admin.style.display = "none";
        normal.style.display = "none";
        return;
    }

    setTimeout(function () {
        window.location.href = "index.html";
    }, 3000);
}