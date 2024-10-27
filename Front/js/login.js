let showPassword = false;

function togglePasswordVisibility() {
  const passwordInput = document.getElementById("password");
  showPassword = !showPassword; // Alterna el valor

  // Cambia el tipo del input
  passwordInput.type = showPassword ? "text" : "password";

  // Cambia el ícono
  const passwordIcon = document.getElementById("password-icon");
  //passwordIcon.textContent = showPassword ? "👁️" : "👁️‍🗨️"; // Cambia entre íconos según la visibilidad
}
