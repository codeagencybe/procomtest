# -*- coding: utf-8 -*-
# from odoo import http


# class HelpdeskTicketSo(http.Controller):
#     @http.route('/helpdesk_ticket_so/helpdesk_ticket_so/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/helpdesk_ticket_so/helpdesk_ticket_so/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpdesk_ticket_so.listing', {
#             'root': '/helpdesk_ticket_so/helpdesk_ticket_so',
#             'objects': http.request.env['helpdesk_ticket_so.helpdesk_ticket_so'].search([]),
#         })

#     @http.route('/helpdesk_ticket_so/helpdesk_ticket_so/objects/<model("helpdesk_ticket_so.helpdesk_ticket_so"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpdesk_ticket_so.object', {
#             'object': obj
#         })
