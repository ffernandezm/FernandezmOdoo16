# -*- coding: utf-8 -*-
# Copyright 2023 PEI

from odoo import fields, models, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    total_projects = fields.Integer(string="Total Projects", compute="_compute_total_projects")
    
    def _compute_total_projects(self):
        for employee in self:
            employee_projects = self.env['employee.project'].search([('employee_id', '=', employee.id)])
            employee.total_projects = len(employee_projects)