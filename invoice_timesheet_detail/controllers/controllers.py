# -*- coding: utf-8 -*-
# from odoo import http


# class InvoiceTimesheetDetail(http.Controller):
#     @http.route('/invoice_timesheet_detail/invoice_timesheet_detail/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_timesheet_detail/invoice_timesheet_detail/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_timesheet_detail.listing', {
#             'root': '/invoice_timesheet_detail/invoice_timesheet_detail',
#             'objects': http.request.env['invoice_timesheet_detail.invoice_timesheet_detail'].search([]),
#         })

#     @http.route('/invoice_timesheet_detail/invoice_timesheet_detail/objects/<model("invoice_timesheet_detail.invoice_timesheet_detail"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_timesheet_detail.object', {
#             'object': obj
#         })
