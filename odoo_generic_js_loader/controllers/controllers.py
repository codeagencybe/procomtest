# -*- coding: utf-8 -*-
# from odoo import http


# class OdooGenericJsLoader(http.Controller):
#     @http.route('/odoo_generic_js_loader/odoo_generic_js_loader/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_generic_js_loader/odoo_generic_js_loader/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_generic_js_loader.listing', {
#             'root': '/odoo_generic_js_loader/odoo_generic_js_loader',
#             'objects': http.request.env['odoo_generic_js_loader.odoo_generic_js_loader'].search([]),
#         })

#     @http.route('/odoo_generic_js_loader/odoo_generic_js_loader/objects/<model("odoo_generic_js_loader.odoo_generic_js_loader"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_generic_js_loader.object', {
#             'object': obj
#         })
