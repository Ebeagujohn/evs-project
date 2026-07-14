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

    if (messages.length > 0) {
        showErrorModal(messages);
    }
});