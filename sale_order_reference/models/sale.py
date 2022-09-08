# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    so_order_reference = fields.Char("Sale Order Reference")

