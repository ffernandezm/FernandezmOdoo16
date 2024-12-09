from odoo.tests.common import HttpCase
from unittest.mock import patch

class TestProjectEmployeeCustomerPortal(HttpCase):

    def setUp(self):
        super().setUp()
        self.employee = self.env['hr.employee'].create({'name': 'Test Employee'})
        self.user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'test_user',
            'employee_ids': [(6, 0, [self.employee.id])]
        })
        self.employee.write({'user_id': self.user.id})

    def test_portal_values(self):
        """Test that portal values are prepared correctly."""
        with patch('odoo.http.request') as mock_request:
            mock_request.env.user = self.user
            controller = self.env['project.customer.portal']
            counters = {'employee_projects_count': True}
            values = controller._prepare_home_portal_values(counters)
            self.assertIn('employee_projects_count', values)
            self.assertEqual(values['employee_projects_count'], 0)

    def test_pagination(self):
        """Test pagination in the employee projects portal."""
        for i in range(15):
            self.env['employee.project'].create({
                'name': f'Project {i}',
                'employee_id': self.employee.id,
            })
        response = self.url_open('/my/employee_projects?page=2', login=self.user.login)
        self.assertEqual(response.status_code, 200, "Pagination failed")
