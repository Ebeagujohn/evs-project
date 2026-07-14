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