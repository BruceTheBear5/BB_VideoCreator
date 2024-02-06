const toggle = document.getElementById("cb3");
const pulse = document.getElementById("#pulse::before");
 

toggle.onchange = function(){
    if(document.body.classList.contains("light-theme")){
        document.body.classList.remove("light-theme");
        pulse.setAttribute("background","linear-gradient(var(--bg),var(--accent),var(--bg))");
    }
    else{
        document.body.classList.add("light-theme");
        pulse.setAttribute("background","linear-gradient(var(--accent),var(--bg),var(--accent))");
    }
}