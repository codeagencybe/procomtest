# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Sale(models.Model):
	
	_inherit = 'sale.order'	

	print_state = fields.Selection([('not-printed', 'Not Printed'),('printed','Printed')], string="Print Status", default="not-printed", required=True)
