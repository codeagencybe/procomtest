# -*- coding: utf-8 -*-
# from odoo import http


# class TimesheetMultilineDescription/(http.Controller):
#     @http.route('/timesheet_multiline_description//timesheet_multiline_description//', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/timesheet_multiline_description//timesheet_multiline_description//objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('timesheet_multiline_description/.listing', {
#             'root': '/timesheet_multiline_description//timesheet_multiline_description/',
#             'objects': http.request.env['timesheet_multiline_description/.timesheet_multiline_description/'].search([]),
#         })

#     @http.route('/timesheet_multiline_description//timesheet_multiline_description//objects/<model("timesheet_multiline_description/.timesheet_multiline_description/"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('timesheet_multiline_description/.object', {
#             'object': obj
#         })
