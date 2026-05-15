document.addEventListener("DOMContentLoaded", function () {
    const banner = document.getElementById("cookie-banner");
    const acceptButton = document.getElementById("cookie-accept");
    const rejectButton = document.getElementById("cookie-reject");

    if (!banner || !acceptButton || !rejectButton) {
        return;
    }

    const consent = localStorage.getItem("casaMilanoCookieConsent");

    if (!consent) {
        banner.hidden = false;
    }

    acceptButton.addEventListener("click", function () {
        localStorage.setItem("casaMilanoCookieConsent", "accepted");
        banner.hidden = true;
    });

    rejectButton.addEventListener("click", function () {
        localStorage.setItem("casaMilanoCookieConsent", "rejected");
        banner.hidden = true;
    });
});