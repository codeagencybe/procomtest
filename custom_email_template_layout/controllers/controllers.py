# -*- coding: utf-8 -*-
# from odoo import http


# class CustomEmailTemplateLayout(http.Controller):
#     @http.route('/custom_email_template_layout/custom_email_template_layout/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_email_template_layout/custom_email_template_layout/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_email_template_layout.listing', {
#             'root': '/custom_email_template_layout/custom_email_template_layout',
#             'objects': http.request.env['custom_email_template_layout.custom_email_template_layout'].search([]),
#         })

#     @http.route('/custom_email_template_layout/custom_email_template_layout/objects/<model("custom_email_template_layout.custom_email_template_layout"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_email_template_layout.object', {
#             'object': obj
#         })
