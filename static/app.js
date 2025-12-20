document.addEventListener("DOMContentLoaded", function () {
    const togglePassword = document.getElementById("togglePassword");
    const passwordField = document.getElementById("password");

    if (togglePassword && passwordField) {
        togglePassword.addEventListener("click", function () {
            const isPasswordHidden = passwordField.type === "password";
            passwordField.type = isPasswordHidden ? "text" : "password";
            this.classList.toggle("active", isPasswordHidden);
        });
    }

    const userInitialsEl = document.getElementById("user-initials");
    if (userInitialsEl) {
        // Si en el futuro quieres setear iniciales desde backend, puedes hacerlo aquí.
        // Por ahora no se fuerza ningún valor para no pisar contenido real.
    }
});


