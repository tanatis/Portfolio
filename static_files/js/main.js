
const profileLink = document.getElementById('profile-icon');
const profileMenu = document.getElementById('profile-menu-wrapper');
profileLink.addEventListener("click", function () {
    profileMenu.classList.toggle("open");
});