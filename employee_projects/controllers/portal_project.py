# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
import json

class PortalEmployeeProject(CustomerPortal):

    @http.route(['/my/employee_projects_kanban'], type='http', auth="user", website=True)
    def portal_my_employee_projects(self, **kwargs):
        employee = request.env.user.employee_id
        projects = request.env['employee.project'].search([('employee_id', '=', employee.id)])
        return request.render('employee_projects.portal_employee_projects', {'projects': projects})

    @http.route(['/my/employee_projects/<int:project_id>'], type='http', auth="user", website=True)
    def portal_employee_project_details(self, project_id, **kwargs):
        project = request.env['employee.project'].sudo().browse(project_id)
        if not project or project.employee_id.id != request.env.user.employee_id.id:
            return request.not_found()
        return request.render('employee_projects.portal_employee_projects_details', {'project': project})
    
    @http.route(['/my/employee_projects/create'], type='http', auth="user", website=True)
    def portal_create_employee_project(self, **kwargs):
        employee = request.env.user.employee_id
        csrf_token = request.csrf_token()
        vals_data = {'employee':employee, 'csrf_token':csrf_token}
        projects = request.env['employee.project'].search([('employee_id', '=', employee.id)])
        return request.render('employee_projects.portal_employee_projects_create', vals_data)

    @http.route(['/my/employee_projects/action_create'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def portal_action_create_employee_project(self, **post):
        employee = request.env.user.employee_id
        data_str = post.get('data')
        #Pasar de string a json
        json_data = json.loads(data_str)
        project_data = {
            'name': json_data.get('name'),
            'description': json_data.get('description'),
            'employee_id': employee.id,
            'start_date': json_data.get('start_date'),
            'end_date': json_data.get('end_date'),
        }
        request.env['employee.project'].sudo().create(project_data)
        return request.redirect('/my/employee_projects')
    
    @http.route(['/my/employee_projects/action_delete/<int:project_id>'], type='http', auth="user", website=True, csrf=True)
    def portal_action_delete_employee_project(self, **post):
        employee = request.env.user.employee_id
        id_project = post.get('project_id')
        #Buscar en employee.project y eliminar ese registro
        request.env['employee.project'].sudo().search([('id', '=', id_project)]).unlink()
        return request.redirect('/my/employee_projects')
