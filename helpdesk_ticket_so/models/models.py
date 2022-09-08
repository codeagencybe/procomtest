# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):

	_inherit = 'sale.order'

	def create_ticket_from_so(self):
		if not self.ticket_id:
			ticket_vals = {'name':self.name,'partner_id':self.partner_id.id}
			ticket = self.env['helpdesk.ticket'].create(ticket_vals)
			self.write({'ticket_id':ticket.id})
		return 