// let toggle = document.getElementById("cb3");
// let pulse = document.getElementById("#pulse::before");

// toggle.onchange = function () {
//     if (document.body.classList.contains("light-theme")) {
//         document.body.classList.remove("light-theme");
//         pulse.setAttribute("background", "linear-gradient(var(--bg),var(--accent),var(--bg))");
//     }
//     else {
//         document.body.classList.add("light-theme");
//         pulse.setAttribute("background", "linear-gradient(var(--accent),var(--bg),var(--accent))");
//     }
// }

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