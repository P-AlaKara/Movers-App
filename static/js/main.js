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

});