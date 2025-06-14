document.addEventListener('DOMContentLoaded', function() {
    const modalCrearEditarLibro = document.getElementById('modalCrearEditarLibro');
    const modalTitle = modalCrearEditarLibro.querySelector('.modal-title');
    const form = document.getElementById('formCrearEditarLibro');
    const libroIdInput = document.getElementById('libroId');
    const nombreInput = document.getElementById('nombre');
    const autorInput = document.getElementById('autor');
    const generoInput = document.getElementById('genero');
    const stockInput = document.getElementById('stock');
    const portadaInput = document.getElementById('portada'); // Ahora es para la URL de la portada

    modalCrearEditarLibro.addEventListener('show.bs.modal', event => {
        const button = event.relatedTarget; // Botón que activó el modal (Agregar o Editar)
        const libroId = button.dataset.libroId; // Obtiene el ID del libro si es edición

        // Limpia el formulario y configura la acción por defecto para "Crear"
        modalTitle.textContent = 'Agregar Nuevo Libro';
        libroIdInput.value = '';
        nombreInput.value = '';
        autorInput.value = '';
        generoInput.value = '';
        stockInput.value = '1'; // Valor por defecto
        portadaInput.value = ''; // Limpia el campo de URL
        form.action = '/libros/crear/'; // Acción por defecto para crear un libro

        // Si se hizo clic en un botón de "Editar Libro"
        if (libroId) {
            modalTitle.textContent = 'Editar Libro'; // Cambia el título del modal
            libroIdInput.value = libroId; // Establece el ID del libro en el campo oculto
            nombreInput.value = button.dataset.libroNombre; // Rellena el nombre
            autorInput.value = button.dataset.libroAutor;   // Rellena el autor
            generoInput.value = button.dataset.libroGenero; // Rellena el género
            stockInput.value = button.dataset.libroStock;   // Rellena el stock

            // Obtiene la URL de la portada del atributo data-* del botón de edición
            const portadaUrl = button.dataset.libroPortadaUrl;
            if (portadaUrl) {
                portadaInput.value = portadaUrl; // Rellena el campo de la URL
            } else {
                portadaInput.value = ''; // Si no hay URL, deja el campo vacío
            }

            // Establece la acción del formulario a la URL de edición para este libro
            form.action = `/libros/editar/${libroId}/`;
        }
    });

});