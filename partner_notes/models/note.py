# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Note(models.Model):
    _inherit = 'note.note'

    partner_id = fields.Many2one('res.partner', 'Customer')

