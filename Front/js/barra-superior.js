// ABRIR SUBMENU AL PRESIONAR EL ICONO DE DROPDOWN
$(document).ready(function () {
  // Al hacer clic en el ícono del menú desplegable
  $(".dropdown-icon").on("click", function () {
    $(this).siblings(".submenu").toggle(); // Muestra u oculta el submenú
  });

  // Manejar clics en las opciones del submenú
  $(".submenu-item").on("click", function () {
    const action = $(this).data("action");
    if (action === "perfil") {
      // Lógica para ir al perfil
      console.log("Ir a Perfil");
      // Aquí puedes redirigir a la página del perfil
    } else if (action === "cerrar-sesion") {
      // Lógica para cerrar sesión
      console.log("Cerrar Sesión");
      // Aquí puedes agregar la lógica para cerrar sesión
    }
  });

  // Cerrar el submenú si se hace clic fuera de él
  $(document).on("click", function (event) {
    if (!$(event.target).closest(".nav-item").length) {
      $(".submenu").hide();
    }
  });
});
