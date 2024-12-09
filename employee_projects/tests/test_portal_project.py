from odoo.tests.common import HttpCase
from unittest.mock import patch
import json


class TestPortalEmployeeProject(HttpCase):

    def setUp(self):
        super().setUp()
        self.employee = self.env['hr.employee'].create({'name': 'Test Employee'})
        self.user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'test_user',
            'employee_ids': [(6, 0, [self.employee.id])]
        })
        self.employee.write({'user_id': self.user.id})
        self.project_model = self.env['employee.project']

    def test_get_portal_projects(self):
        """Test the route that displays the kanban view of employee projects."""
        with self.env.cr.savepoint(), self.registry.cursor() as cr:
            # Simulate a session with the user logged in
            self.start_tour('/my/employee_projects_kanban', 'main')

    def test_create_project(self):
        """Test project creation via portal."""
        project_data = {
            'name': 'Test Project',
            'description': 'Description of test project',
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
        }
        data_json = json.dumps(project_data)
        response = self.url_open(
            '/my/employee_projects/action_create',
            data={'data': data_json},
            login=self.user.login
        )
        self.assertEqual(response.status_code, 200, "Project creation failed")

    def test_delete_project(self):
        """Test project deletion via portal."""
        project = self.project_model.create({
            'name': 'Project to Delete',
            'employee_id': self.employee.id,
        })
        self.url_open(
            f'/my/employee_projects/action_delete/{project.id}',
            login=self.user.login
        )
        project_exists = self.project_model.search([('id', '=', project.id)])
        self.assertFalse(project_exists, "Project was not deleted")
