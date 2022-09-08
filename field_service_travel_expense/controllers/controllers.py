# -*- coding: utf-8 -*-
# from odoo import http


# class FieldServiceTravelExpense(http.Controller):
#     @http.route('/field_service_travel_expense/field_service_travel_expense/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/field_service_travel_expense/field_service_travel_expense/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('field_service_travel_expense.listing', {
#             'root': '/field_service_travel_expense/field_service_travel_expense',
#             'objects': http.request.env['field_service_travel_expense.field_service_travel_expense'].search([]),
#         })

#     @http.route('/field_service_travel_expense/field_service_travel_expense/objects/<model("field_service_travel_expense.field_service_travel_expense"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('field_service_travel_expense.object', {
#             'object': obj
#         })
