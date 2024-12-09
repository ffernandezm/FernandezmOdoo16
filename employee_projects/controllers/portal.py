# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from operator import itemgetter

from odoo import http, _
from odoo.http import request
from odoo.osv.expression import AND, OR
from odoo.tools import groupby as groupbyelem

from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager

from collections import OrderedDict
from dateutil.relativedelta import relativedelta
from operator import itemgetter



class ProjectEmployeeCustomerPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        if 'employee_projects_count' in counters:
            domain = self._get_portal_default_domain()
            values['employee_projects_count'] = len(request.env['employee.project'].search(domain))

        return values

    def _get_portal_default_domain(self):
        my_user = request.env.user
        employee_id = my_user.employee_id
        if employee_id:
            return [
                ('employee_id', '=', employee_id.id)
            ]
        else:
            return [('employee_id', '=', False)]
    
    def _prepare_employee_project_domain(self):
        return []

    def _prepare_searchbar_sortings(self):
        return {
            'name': {'label': _('Name'), 'order': 'name'},
        }

    @http.route(['/my/employee_projects', '/my/employee_projects/page/<int:page>'], type='http', auth="user", website=True, csrf=True)
    def portal_my_employee_projects(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        employee_project = request.env['employee.project']
        domain = self._prepare_employee_project_domain()

        searchbar_sortings = self._prepare_searchbar_sortings()
        if not sortby:
            sortby = 'name'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # projects count
        domain = self._get_portal_default_domain()
        employee_project_count = len(request.env['employee.project'].search(domain))
        # pager
        pager = portal_pager(
            url="/my/employee_projects",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=employee_project_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        employee_project = employee_project.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_employee_projects_history'] = employee_project.ids[:100]
        csrf_token = request.csrf_token()
        values.update({
            'csrf_token': csrf_token,
            'date': date_begin,
            'date_end': date_end,
            'employee_projects': employee_project,
            'page_name': 'project',
            'default_url': '/my/employee_projects',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("employee_projects.portal_my_employee_projects", values)
