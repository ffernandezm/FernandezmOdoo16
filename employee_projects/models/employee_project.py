# -*- coding: utf-8 -*-
# Copyright 2023 PEI

from odoo import fields, models, api

class EmployeeProject(models.Model):
    _name = 'employee.project'

    name = fields.Char(string="Project Name", required=True)
    description = fields.Text(string="Description")
    employee_id = fields.Many2one('hr.employee', string="Employee Name", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End date", required=True)