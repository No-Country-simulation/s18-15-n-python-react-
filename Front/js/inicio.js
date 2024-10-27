//Cuando la parte visual este hecha, aqui empieza fetching de datos para este componente
// Selecciona los botones
const btnVistaLista = document.getElementById('vista-lista');
const btnVistaCuadricula = document.getElementById('vista-cuadricula');

// Función para manejar el cambio de vista y color
function toggleSelectedView(selectedButton) {
    // Remueve la clase 'selected' de ambos botones
    btnVistaLista.classList.remove('selected');
    btnVistaCuadricula.classList.remove('selected');

    // Agrega la clase 'selected' solo al botón clickeado
    selectedButton.classList.add('selected');
}

// Asignar los eventos de clic a los botones
btnVistaLista.addEventListener('click', function() {
    toggleSelectedView(btnVistaLista);
});

btnVistaCuadricula.addEventListener('click', function() {
    toggleSelectedView(btnVistaCuadricula);
});
