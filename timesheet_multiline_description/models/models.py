# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TimesheetMultiLine(models.Model):

	_inherit = 'account.analytic.line'

	name = fields.Text(required=True)