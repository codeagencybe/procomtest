# -*- coding: utf-8 -*-
# from odoo import http


# class HelpdeskFilterCustom(http.Controller):
#     @http.route('/helpdesk_filter_custom/helpdesk_filter_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/helpdesk_filter_custom/helpdesk_filter_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpdesk_filter_custom.listing', {
#             'root': '/helpdesk_filter_custom/helpdesk_filter_custom',
#             'objects': http.request.env['helpdesk_filter_custom.helpdesk_filter_custom'].search([]),
#         })

#     @http.route('/helpdesk_filter_custom/helpdesk_filter_custom/objects/<model("helpdesk_filter_custom.helpdesk_filter_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpdesk_filter_custom.object', {
#             'object': obj
#         })
