# -*- coding: utf-8 -*-
import json
from odoo import http, SUPERUSER_ID
from odoo.addons.web.controllers.main import ReportController
from odoo.http import request

class ReportControllerCustom(ReportController):
    
    @http.route([
        '/report/<converter>/<reportname>',
        '/report/<converter>/<reportname>/<docids>',
    ], type='http', auth='user', website=True)
    def report_routes(self, reportname, docids=None, converter=None, **data):
        res = super(ReportControllerCustom, self).report_routes(reportname=reportname, docids=docids, converter=converter, data=data)
        if reportname == 'sale.report_saleorder':
            try:
                docids = [int(id) for id in docids.split(',')]
                orders = request.env['sale.order'].browse(docids)
                for order in orders:
                    order.write({'print_state':'printed'})
            except:
                pass
        return res