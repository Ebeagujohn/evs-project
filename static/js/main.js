// static/js/main.js — shared across all apps
function showErrorModal(messages) {
    var backdrop = document.getElementById("error-modal-backdrop");
    var list = document.getElementById("error-modal-list");
    var closeBtn = document.getElementById("error-modal-close");

    list.innerHTML = "";
    messages.forEach(function (msg) {
        var li = document.createElement("li");
        li.textContent = msg;
        list.appendChild(li);
    });

    backdrop.style.display = "flex";

    closeBtn.onclick = function () {
        backdrop.style.display = "none";
    };
    backdrop.onclick = function (e) {
        if (e.target === backdrop) backdrop.style.display = "none";
    };
}

// Hamburger menu toggle — shows/hides the dropdown nav (Register/Vote/Results/Admin)
document.addEventListener("DOMContentLoaded", function () {
    var toggleBtn = document.getElementById("menu-toggle");
    var nav = document.getElementById("site-nav");
    if (!toggleBtn || !nav) return;

    toggleBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        nav.classList.toggle("open");
    });

    document.addEventListener("click", function (e) {
        if (nav.classList.contains("open") && !nav.contains(e.target) && e.target !== toggleBtn) {
            nav.classList.remove("open");
        }
    });
});