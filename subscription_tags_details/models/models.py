# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Subscription(models.Model):

	_inherit = 'sale.subscription'

	memo = fields.Char("Internal Memo")

class SubscriptionTag(models.Model):

	_inherit = 'account.analytic.tag'

class SubscriptionTagDistribution(models.Model):

	_inherit = 'account.analytic.distribution'