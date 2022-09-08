# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date
from dateutil.relativedelta import relativedelta


class HelpdeskTicket(models.Model):

    _inherit = 'helpdesk.ticket'

    reference = fields.Char(default=_("New"))

    @api.model
    def create(self, vals):
        """
        """
        vals['reference'] = self.env['ir.sequence'].next_by_code('seq.helpdesk.ticket') or _('New')
        res = super(HelpdeskTicket, self).create(vals)
        return res
