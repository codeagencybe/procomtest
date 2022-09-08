# -*- coding: utf-8 -*-
import json
from odoo import http, SUPERUSER_ID
from odoo.addons.web.controllers.main import ExcelExport, serialize_exception
from odoo.http import request

class ExcelExportCustom(ExcelExport):

    @http.route(['/web/export/timesheet-xlsx'], type='http', auth="public", methods=['POST'], website=True)
    def timesheet_xlsx_custom(self, **kw):
        order = request.env['sale.order'].sudo().browse(int(kw.get('order')))
        data = {
            "model": "account.analytic.line",
            "fields": [
                {
                  "name": "date",
                  "label": "Date",
                  "store": True,
                  "type": "date"
                },
                {
                  "name": "employee_id",
                  "label": "Employee",
                  "store": True,
                  "type": "many2one"
                },
                {
                  "name": "project_id",
                  "label": "Project",
                  "store": True,
                  "type": "many2one"
                },
                {
                  "name": "task_id",
                  "label": "Task",
                  "store": True,
                  "type": "many2one"
                },
                {
                  "name": "name",
                  "label": "Description",
                  "store": True,
                  "type": "char"
                },
                {
                  "name": "unit_amount",
                  "label": "Quantity",
                  "store": True,
                  "type": "float"
                }
                ],
                "ids": False,
                "domain":["&",["so_line","in",order.order_line.ids],"&",["so_line","!=",False],["non_allow_billable","=",False]],
            "groupby": [],
            "context": {
            "lang": "en_US",
            "tz": "Asia/Calcutta",
            "uid": request.uid,
            "allowed_company_ids": request.env['res.company'].sudo().search([]).ids,
            "active_id": order.project_id.id,
            "active_ids": order.project_id.ids,
            "params": {
              "action": request.env.ref('sale_timesheet.timesheet_action_from_sales_order').id,
              "active_id": order.project_id.id,
              "cids": request.env.user.company_id.id,
              "menu_id":  request.env.ref('project.menu_main_pm').id,
              "model": "account.analytic.line",
              "view_type": "list"
            }
            },
            "import_compat": False
        }
        token = kw.get('token')
        uid = request.uid
        request.uid = SUPERUSER_ID
        res = self.base(json.dumps(data), token)
        request.uid = uid
        return res