//No tocar este codigo, se encarga de que la navegación basica del sitio web funcione

const DOM = document;

DOM.querySelectorAll(".nav-item").forEach((item) => {
  item.addEventListener("click", function () {
    const page = this.dataset.page; // Obtiene el valor de data-page
    DOM.getElementById("page-title").textContent = this.textContent.trim();

    // Oculta todos los componentes
    DOM.querySelectorAll(".component").forEach((component) => {
      component.style.display = "none";
    });

    // Muestra el componente correspondiente
    DOM.getElementById(page).style.display = "block";
  });
});
