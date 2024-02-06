let signin = document.getElementById("signin");
let signup = document.getElementById("signup");

function toggleForms() {
    if (signin.style.display === "none") {
        signin.style.display = "flex";
        signup.style.display = "none";
    } else {
        signin.style.display = "none";
        signup.style.display = "flex";
    }
}