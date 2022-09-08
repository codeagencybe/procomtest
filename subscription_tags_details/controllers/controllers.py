# -*- coding: utf-8 -*-
# from odoo import http


# class SubscriptionTagsDetails(http.Controller):
#     @http.route('/subscription_tags_details/subscription_tags_details/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/subscription_tags_details/subscription_tags_details/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('subscription_tags_details.listing', {
#             'root': '/subscription_tags_details/subscription_tags_details',
#             'objects': http.request.env['subscription_tags_details.subscription_tags_details'].search([]),
#         })

#     @http.route('/subscription_tags_details/subscription_tags_details/objects/<model("subscription_tags_details.subscription_tags_details"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('subscription_tags_details.object', {
#             'object': obj
#         })
