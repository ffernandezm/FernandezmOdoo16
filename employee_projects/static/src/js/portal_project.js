odoo.define('employee_projects.portal_project', function (require) {
    "use strict";

    const ajax = require('web.ajax');
    console.log('Portal Project Module ######');

    // Escuchar el evento de clic en el botón de crear proyecto
    document.querySelector('#create_project_button').addEventListener('click', function (event) {
        event.preventDefault(); // Prevenir el envío convencional del formulario

        // Obtener datos del formulario
        const projectData = {
            name: document.querySelector('#name').value,
            description: document.querySelector('#description').value,
            start_date: document.querySelector('#start_date').value,
            end_date: document.querySelector('#end_date').value,
        };

        // Obtener el token CSRF desde el campo oculto en la página
        const csrfToken = document.querySelector('#csrf_token')?.value;

        if (!csrfToken) {
            console.error('CSRF token not found.');
            return;
        }

        // Enviar los datos a través de AJAX con el token CSRF
        ajax.post('/my/employee_projects/action_create', {
            data: JSON.stringify(projectData), // Convertir el objeto a JSON
            csrf_token: csrfToken, // Incluir el token CSRF
        }).then(function () {
            // Redirigir después de que el proyecto haya sido creado
            window.location.href = '/my/employee_projects';
        }).catch(function (error) {
            console.error('Error al crear el proyecto:', error);
        });
    });
});
