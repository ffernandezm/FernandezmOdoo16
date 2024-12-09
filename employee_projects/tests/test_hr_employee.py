from odoo.tests.common import TransactionCase

class TestHrEmployee(TransactionCase):
    def setUp(self):
        super(TestHrEmployee, self).setUp()
        self.employee = self.env['hr.employee'].create({'name': 'Test Employee'})
        self.project1 = self.env['employee.project'].create({
            'name': 'Project 1',
            'employee_id': self.employee.id,
        })
        self.project2 = self.env['employee.project'].create({
            'name': 'Project 2',
            'employee_id': self.employee.id,
        })

    def test_total_projects_computation(self):
        """Verifica que el cálculo total de proyectos sea correcto."""
        self.employee._compute_total_projects()
        self.assertEqual(self.employee.total_projects, 2, "El total de proyectos no es correcto.")
