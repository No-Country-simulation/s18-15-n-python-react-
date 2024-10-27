const editBtn = document.getElementById("editBtn");
const discardBtn = document.getElementById("discardBtn");
const passwordFields = document.getElementById("passwordFields");
const passwordStaticRow = document.getElementById("passwordStaticRow");
let isEditing = false;

function toggleEditMode(enable) {
  const spans = document.querySelectorAll(".data-value:not(input)");

  if (enable) {
    spans.forEach((span) => {
      if (span.id !== "passwordSpan") {
        const value = span.textContent;
        const input = document.createElement("input");
        input.type = "text";
        input.placeholder = value;
        input.className = "data-value";
        span.parentNode.replaceChild(input, span);
      }
    });

    passwordStaticRow.style.display = "none";
    passwordFields.style.display = "block";

    editBtn.innerHTML = `
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                        <polyline points="17 21 17 13 7 13 7 21"></polyline>
                        <polyline points="7 3 7 8 15 8"></polyline>
                    </svg>
                    Guardar
                `;
    discardBtn.style.display = "flex";
  } else {
    const inputs = document.querySelectorAll(
      'input.data-value:not([type="password"])'
    );
    inputs.forEach((input) => {
      if (input.parentNode) {
        const span = document.createElement("span");
        span.id =
          input.parentNode
            .querySelector(".data-label")
            .textContent.slice(0, -1)
            .toLowerCase() + "Span";
        span.className = "data-value";
        span.textContent = input.value || input.placeholder;
        input.parentNode.replaceChild(span, input);
      }
    });

    passwordStaticRow.style.display = "flex";
    passwordFields.style.display = "none";

    editBtn.innerHTML = `
<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#000000"><path d="M200-200h57l391-391-57-57-391 391v57Zm-80 80v-170l528-527q12-11 26.5-17t30.5-6q16 0 31 6t26 18l55 56q12 11 17.5 26t5.5 30q0 16-5.5 30.5T817-647L290-120H120Zm640-584-56-56 56 56Zm-141 85-28-29 57 57-29-28Z"/></svg>
                    Editar
                `;
    discardBtn.style.display = "none";
  }
}

editBtn.addEventListener("click", () => {
  isEditing = !isEditing;
  toggleEditMode(isEditing);
});

discardBtn.addEventListener("click", () => {
  isEditing = false;
  toggleEditMode(false);
  // Limpiar los campos de contraseña
  document.getElementById("currentPassword").value = "";
  document.getElementById("newPassword").value = "";
  document.getElementById("confirmPassword").value = "";
});
