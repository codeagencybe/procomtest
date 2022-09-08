# -*- coding: utf-8 -*-
# from odoo import http


# class SubscriptionFreequencyListView(http.Controller):
#     @http.route('/subscription_freequency_list_view/subscription_freequency_list_view/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/subscription_freequency_list_view/subscription_freequency_list_view/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('subscription_freequency_list_view.listing', {
#             'root': '/subscription_freequency_list_view/subscription_freequency_list_view',
#             'objects': http.request.env['subscription_freequency_list_view.subscription_freequency_list_view'].search([]),
#         })

#     @http.route('/subscription_freequency_list_view/subscription_freequency_list_view/objects/<model("subscription_freequency_list_view.subscription_freequency_list_view"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('subscription_freequency_list_view.object', {
#             'object': obj
#         })
