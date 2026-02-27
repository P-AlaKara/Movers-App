document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".is-danger").forEach(button => {
        if (button.textContent.trim().toLowerCase() === "cancel") {
            button.addEventListener("click", function (e) {
                const confirmed = confirm("Are you sure you want to cancel?");
                if (!confirmed) {
                    e.preventDefault();
                }
            });
        }
    });

    // hamburger menu toggle for mobile
    const burger = document.querySelector('.navbar-burger');
    const menu = document.getElementById('navbarBasic');
    if (burger && menu) {
        burger.addEventListener('click', () => {
            burger.classList.toggle('is-active');
            menu.classList.toggle('is-active');
        });
    }
});