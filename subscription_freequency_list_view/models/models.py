# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SubscriptionSale(models.Model):

	_inherit = "sale.subscription"


	@api.depends('template_id')
	def _compute_subscription_frequency(self):
		for subscription in self:
			frequency = str()
			if subscription.template_id:
				frequency = subscription.template_id.recurring_rule_type.title()
			subscription.update({
					'frequency':frequency,
				})

	frequency = fields.Char("Subscription Frequency", compute="_compute_subscription_frequency")