// static/prestamos/prestamos.js
document.addEventListener('DOMContentLoaded', function() {
    const btnNuevoPrestamo = document.querySelector('.btn-crear-prestamo');
    const modalNuevoPrestamoEl = document.getElementById('modalNuevoPrestamo');
    const formNuevoPrestamo = document.getElementById('formNuevoPrestamo');
    const tablaPrestamosBody = document.getElementById('tabla-prestamos-body');
    const formErrorsDiv = document.getElementById('form-errors');

    const modalEditarPrestamoEl = document.getElementById('modalEditarPrestamo');
    const formEditarPrestamo = document.getElementById('formEditarPrestamo');
    const editarFormFieldsDiv = document.getElementById('editar-form-fields');
    const editarFormErrorsDiv = document.getElementById('editar-form-errors');
    let prestamoIdAEditar = null;

    const modalEliminarPrestamoEl = document.getElementById('modalEliminarPrestamo');
    const btnConfirmarEliminar = document.getElementById('btnConfirmarEliminar');
    const btnCancelarEliminar = document.getElementById('btnCancelarEliminar');
    let prestamoIdAEliminar = null;


    function createModalStateManager(modalEl, formToReset = null) {
        let isModalShown = false;

        modalEl.addEventListener('show.bs.modal', function() {
            console.log('Evento show.bs.modal disparado para:', modalEl.id);
            isModalShown = true;
        });

        modalEl.addEventListener('hidden.bs.modal', function() {
            console.log('Evento hidden.bs.modal disparado para:', modalEl.id);
            if (isModalShown) {
                console.log('El modal estaba realmente mostrado, realizando limpieza.');
                document.body.classList.remove('modal-open');
                document.body.style.overflow = '';
                const modalBackdrop = document.querySelector('.modal-backdrop');
                if (modalBackdrop) {
                    console.log('Eliminando backdrop:', modalBackdrop);
                    modalBackdrop.remove();
                } else {
                    console.log('No se encontró el backdrop para eliminar.');
                }
                if (formToReset) {
                    formToReset.reset();
                }
            } else {
                console.log('El modal no estaba mostrado, no se requiere limpieza.');
            }
            isModalShown = false;
        });

        return {
            open: function(formErrors = null) {
                console.log('Abriendo modal:', modalEl.id);
                const modal = new bootstrap.Modal(modalEl);
                modal.show();
                if (formErrors) {
                    formErrors.innerHTML = '';
                }
            }
        };
    }

    const nuevoPrestamoModal = createModalStateManager(modalNuevoPrestamoEl, formNuevoPrestamo);
    const editarPrestamoModal = createModalStateManager(modalEditarPrestamoEl);
    const eliminarPrestamoModal = createModalStateManager(modalEliminarPrestamoEl);


    btnNuevoPrestamo.addEventListener('click', function() {
        nuevoPrestamoModal.open(formErrorsDiv);
    });

    formNuevoPrestamo.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);

        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const newRow = tablaPrestamosBody.insertRow(0);
                newRow.id = `prestamo-${data.prestamo.id}`;
                newRow.innerHTML = `
                    <td>${data.prestamo.libro}</td>
                    <td>${data.prestamo.nombre_persona}</td>
                    <td>${data.prestamo.curso}</td>
                    <td>${data.prestamo.rut}</td>
                    <td>${data.prestamo.celular}</td>
                    <td>${data.prestamo.fecha_prestamo}</td>
                    <td>${data.prestamo.fecha_devolucion}</td>
                    <td class="crud-actions text-center">
                        <button class="btn btn-sm btn-warning btn-editar-prestamo"
                                data-bs-toggle="modal"
                                data-bs-target="#modalEditarPrestamo"
                                data-prestamo-id="${data.prestamo.id}">
                            <i class="fas fa-edit"></i> Editar
                        </button>
                        <button class="btn btn-sm btn-danger btn-eliminar-prestamo"
                                data-bs-toggle="modal"
                                data-bs-target="#modalEliminarPrestamo"
                                data-prestamo-id="${data.prestamo.id}">
                            <i class="fas fa-trash-alt"></i> Eliminar
                        </button>
                    </td>
                `;
                const modal = bootstrap.Modal.getInstance(modalNuevoPrestamoEl);
                modal.hide();
            } else {
                let errorsHtml = '<ul>';
                for (const field in data.errors) {
                    data.errors[field].forEach(error => {
                        errorsHtml += `<li>${field}: ${error}</li>`;
                    });
                }
                errorsHtml += '</ul>';
                formErrorsDiv.innerHTML = errorsHtml;
            }
        })
        .catch(error => {
            console.error('Error en la petición AJAX de creación:', error);
            alert('Ocurrió un error al enviar la petición de creación.');
        });
    });

    tablaPrestamosBody.addEventListener('click', function(event) {
        if (event.target.classList.contains('btn-editar-prestamo')) {
            prestamoIdAEditar = event.target.dataset.prestamoId;
            console.log('ID del préstamo a editar (GET):', prestamoIdAEditar);
            fetch(`/prestamos/editar/${prestamoIdAEditar}/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                console.log('Respuesta del servidor para editar (GET):', response);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Datos recibidos para editar (GET):', data);
                if (data.success) {
                    editarFormFieldsDiv.innerHTML = data.form_html;
                    editarPrestamoModal.open(editarFormErrorsDiv);
                } else {
                    alert('Error al cargar los datos del préstamo para editar. ' + (data.error || ''));
                    console.error('Error del servidor al cargar datos de edición (GET):', data.error);
                }
            })
            .catch(error => {
                console.error('Error en la petición AJAX de edición (GET):', error);
                alert('Ocurrió un error al obtener los datos del préstamo. Verifique la consola para más detalles.');
            });
        } else if (event.target.classList.contains('btn-eliminar-prestamo')) {
            prestamoIdAEliminar = event.target.dataset.prestamoId;
            eliminarPrestamoModal.open();
        }
    });

    formEditarPrestamo.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);

        // Obtener el token CSRF directamente del campo oculto dentro del formulario
        const csrfToken = formEditarPrestamo.querySelector('input[name="csrfmiddlewaretoken"]').value;

        const urlEditar = `/prestamos/editar/${prestamoIdAEditar}/`;
        console.log('Enviando datos para editar (POST) a:', urlEditar);
        console.log('Datos del formulario:', Object.fromEntries(formData.entries()));

        fetch(urlEditar, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => {
            console.log('Respuesta del servidor para editar (POST):', response);
            if (!response.ok) {
                return response.text().then(text => { throw new Error(`HTTP error! status: ${response.status}, message: ${text}`); });
            }
            return response.json();
        })
        .then(data => {
            console.log('Datos recibidos después de editar (POST):', data);
            if (data.success) {
                const rowToUpdate = document.getElementById(`prestamo-${prestamoIdAEditar}`);
                if (rowToUpdate) {
                    rowToUpdate.innerHTML = `
                        <td>${data.prestamo.libro}</td>
                        <td>${data.prestamo.nombre_persona}</td>
                        <td>${data.prestamo.curso}</td>
                        <td>${data.prestamo.rut}</td>
                        <td>${data.prestamo.celular}</td>
                        <td>${data.prestamo.fecha_prestamo}</td>
                        <td>${data.prestamo.fecha_devolucion}</td>
                        <td class="crud-actions text-center">
                            <button class="btn btn-sm btn-warning btn-editar-prestamo"
                                    data-bs-toggle="modal"
                                    data-bs-target="#modalEditarPrestamo"
                                    data-prestamo-id="${data.prestamo.id}">
                                <i class="fas fa-edit"></i> Editar
                            </button>
                            <button class="btn btn-sm btn-danger btn-eliminar-prestamo"
                                    data-bs-toggle="modal"
                                    data-bs-target="#modalEliminarPrestamo"
                                    data-prestamo-id="${data.prestamo.id}">
                                <i class="fas fa-trash-alt"></i> Eliminar
                            </button>
                        </td>
                    `;
                } else {
                    console.warn('Fila a actualizar no encontrada:', `prestamo-${prestamoIdAEditar}`);
                }
                const modal = bootstrap.Modal.getInstance(modalEditarPrestamoEl);
                modal.hide();
                prestamoIdAEditar = null; 
            } else {
                let errorsHtml = '<ul>';
                for (const field in data.errors) {
                    data.errors[field].forEach(error => {
                        errorsHtml += `<li>${field}: ${error}</li>`;
                    });
                }
                errorsHtml += '</ul>';
                editarFormErrorsDiv.innerHTML = errorsHtml;
                console.error('Errores de validación del formulario:', data.errors);
            }
        })
        .catch(error => {
            console.error('Error al enviar la petición de edición (POST):', error);
            alert('Ocurrió un error al guardar los cambios. Verifique la consola para más detalles.');
        });
    });

    btnCancelarEliminar.addEventListener('click', function() {
        const modal = bootstrap.Modal.getInstance(modalEliminarPrestamoEl);
        modal.hide();
        prestamoIdAEliminar = null;
    });

    btnConfirmarEliminar.addEventListener('click', function() {
        if (prestamoIdAEliminar) {
            fetch(`/prestamos/eliminar/${prestamoIdAEliminar}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ 'prestamo_id': prestamoIdAEliminar })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const rowToRemove = document.getElementById(`prestamo-${prestamoIdAEliminar}`);
                    if (rowToRemove) {
                        rowToRemove.remove();
                    }
                    const modal = bootstrap.Modal.getInstance(modalEliminarPrestamoEl);
                    modal.hide();
                    prestamoIdAEliminar = null;
                } else {
                    alert('Error al eliminar el préstamo.');
                    console.error('Error:', data.error);
                }
            })
            .catch(error => {
                console.error('Error en la petición AJAX de eliminación:', error);
                alert('Ocurrió un error al intentar eliminar el préstamo.');
            });
        }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
            return cookieValue;
        }
    }
});