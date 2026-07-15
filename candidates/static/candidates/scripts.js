// candidates/static/candidates/scripts.js
document.addEventListener("DOMContentLoaded", function () {
    var errorsEl = document.getElementById("form-errors");
    if (!errorsEl) return;

    var errors = JSON.parse(errorsEl.textContent);
    var messages = [];

    for (var field in errors) {
        errors[field].forEach(function (msg) {
            messages.push(field + ": " + msg);
        });
    }

    // Non-field errors (like the duplicate-candidate check) are grouped
    // under the key "__all__" by Django — label them plainly.
    if (errors["__all__"]) {
        messages = messages.filter(function (m) { return m.indexOf("__all__:") !== 0; });
        errors["__all__"].forEach(function (msg) {
            messages.push(msg);
        });
    }

    if (messages.length > 0) {
        showErrorModal(messages);
    }
});