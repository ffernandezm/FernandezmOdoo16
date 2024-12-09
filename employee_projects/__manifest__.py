# -*- coding: utf-8 -*-

{
    'name': "Employee Projects",

    'summary': """
        Desarrollo que Hr donde se asignan proyectos a empleados""",

    'description': """
        Desarrollo que extiende modulo de Hr y Portal donde
        se administran proyectos a empleados en un nuevo modelo, tanto
        en la aplicacion de Hr como en el Portal""",

    "author": "Fernando Fernández nffernandezm@gmail.com",
    'version': '16.0.0.0.1',

    # Dependencias
    'depends': [
        'hr',
        'portal',
    ],

    # Data
    'data': [
        'views/hr_employee_views.xml',
        'views/employee_project_views.xml',
        'views/portal_project_templates.xml',
        'views/portal_templates.xml',
        'data/data_employee_project.xml',
        'security/account_groups.xml',
        'security/ir.model.access.csv',
    ],
    
    'assets': {
        'web.assets_frontend': [
            'employee_projects/static/src/js/portal_project.js',
        ],
    },
}
