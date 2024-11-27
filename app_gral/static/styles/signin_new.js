/*
document.addEventListener("DOMContentLoaded", function() {
    const btnSignIn = document.getElementById("sign-in");
    const btnSignUp = document.getElementById("sign-up");
    const formRegister = document.querySelector(".register");
    const formLogin = document.querySelector(".login");
    const homeButton = document.getElementById("home-button");

    if (btnSignIn && btnSignUp && formRegister && formLogin && homeButton) {
        btnSignIn.addEventListener("click", function() {
            formRegister.classList.add("hide");
            formLogin.classList.remove("hide");
        });

        btnSignUp.addEventListener("click", function() {
            formLogin.classList.add("hide");
            formRegister.classList.remove("hide");
        });

        homeButton.addEventListener("click", function() {
            window.location.href = "{% url 'home' %}";
        });
    } else {
        console.error("No se encontraron todos los elementos necesarios.");
    }
});
 */
