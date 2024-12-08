const body = document.querySelector('body'),
      sidebar = body.querySelector('nav'),
      toggle = body.querySelector(".toggle"),
      searchBtn = body.querySelector(".search-box"),
      modeSwitch = body.querySelector(".toggle-switch"),
      modeText = body.querySelector(".mode-text");



// Cambiar el tema al hacer clic en el botón de alternar
modeSwitch.addEventListener("click", () => {
    body.classList.toggle("dark");

    // Cambiar el texto del modo según el tema
    if (body.classList.contains("dark")) {
        modeText.innerText = "Modo Claro";
        localStorage.setItem("theme", "dark");  // Guardar el tema oscuro en el almacenamiento local
    } else {
        modeText.innerText = "Modo Oscuro";
        localStorage.setItem("theme", "light");  // Guardar el tema claro en el almacenamiento local
    }
});

// Cargar el tema al cargar la página
document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {
        body.classList.add("dark");
        modeText.innerText = "CLARO";
    } else {
        body.classList.remove("dark");
        modeText.innerText = "OSCURO";
    }
});

// Alternar el sidebar al hacer clic en el botón de toggle
toggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
});

// // Eliminar la clase close del sidebar al hacer clic en el campo de búsqueda
// searchBtn.addEventListener("click", () => {
//     sidebar.classList.remove("close");
// });
