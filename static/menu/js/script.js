document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".show-comment-form").forEach(function (button) {
        button.addEventListener("click", function () {
            const dishId = this.dataset.dishId;

            const commentsList = document.getElementById("commentsList" + dishId);
            const commentForm = document.getElementById("commentForm" + dishId);

            if (commentsList && commentForm) {
                commentsList.classList.add("d-none");
                commentForm.classList.remove("d-none");
            }
        });
    });

    document.querySelectorAll(".hide-comment-form").forEach(function (button) {
        button.addEventListener("click", function () {
            const dishId = this.dataset.dishId;

            const commentsList = document.getElementById("commentsList" + dishId);
            const commentForm = document.getElementById("commentForm" + dishId);

            if (commentsList && commentForm) {
                commentForm.classList.add("d-none");
                commentsList.classList.remove("d-none");
            }
        });
    });
});