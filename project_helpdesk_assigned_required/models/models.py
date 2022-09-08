# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Helpsdesk(models.Model):
    _inherit = 'helpdesk.ticket'

    user_id = fields.Many2one(
        'res.users', string='Assigned to', compute='_compute_user_and_stage_ids', store=True,
        readonly=False, tracking=True, required=True, default=lambda self: self.env.uid, 
        domain=lambda self: [('groups_id', 'in', self.env.ref('helpdesk.group_helpdesk_user').id)])


class ProjectTask(models.Model):
    _inherit = 'project.task'

    user_id = fields.Many2one('res.users', string='Assigned to',
                              default=lambda self: self.env.uid, index=True, tracking=True, required=True)
