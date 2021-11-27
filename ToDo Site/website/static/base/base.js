const links = document.querySelector(".navbar-links")

function toggle() {
    links.classList.toggle("navbar-links")
    links.classList.toggle("navbar-links-active")
}
/*-----TOGGLING NAVBAR-----*/
const errorDiv = document.getElementById("errorDiv")

function closeError() {
    errorDiv.style.display = "none"
}
/*-----CLOSING ERROR MESSAGE-----*/
const successDiv = document.getElementById("successDiv")

function closeSuccess() {
    successDiv.style.display = "none"
}
/*----- CLOSING SUCCESS MESSAGE-----*/