# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Invoice(models.Model):

    _inherit = 'account.move'

    def get_orders(self):
        sale_lines = [x.sale_line_ids for x in self.line_ids]
        sale_orders = [line.order_id for line in sale_lines if line.order_id]
        if sale_orders:
            return sale_orders[0]
        return []


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'