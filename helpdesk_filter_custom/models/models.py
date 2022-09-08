# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelpdeskTicket(models.Model):
    
    _inherit = 'helpdesk.ticket'

    @api.depends('tag_ids', 'stage_id.is_close','stage_id','stage_id.name', 'sale_order_id', 'timesheet_ids')
    def _compute_is_tag_billable(self):
        for ticket in self:
            is_tag_billable = False
            if any([tag.name for tag in ticket.tag_ids if tag.name in ['billable','Billable']]):
                if ticket.stage_id.is_close and not ticket.sale_order_id and ticket.timesheet_ids:
                    is_tag_billable = True
            ticket.update({
                    'is_tag_billable':is_tag_billable,
                })

    is_tag_billable = fields.Boolean(compute="_compute_is_tag_billable", store=True)
