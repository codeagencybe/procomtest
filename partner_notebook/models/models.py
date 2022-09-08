# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):

    _inherit = 'res.partner'
    
    contact_info = fields.Html("Credentials/Other Info")


class HelpdeskTicket(models.Model):

    _inherit = 'helpdesk.ticket'
    

    @api.depends('partner_id')
    def _get_contact_info(self):
        for ticket in self:
            if ticket.partner_id.company_type == 'company':
                contact_info = ticket.partner_id.contact_info
            else:
                contact_info = ticket.partner_id.parent_id.contact_info

            ticket.update({
                    'contact_info':contact_info
                })

    contact_info = fields.Html("Credentials/Other Info", compute="_get_contact_info")


class ProjectTask(models.Model):

    _inherit = 'project.task'
    
    @api.depends('partner_id')
    def _get_contact_info(self):
        for task in self:
            if task.partner_id.company_type == 'company':
                contact_info = task.partner_id.contact_info
            else:
                contact_info = task.partner_id.parent_id.contact_info

            task.update({
                    'contact_info':contact_info
                })


    contact_info = fields.Html("Credentials/Other Info", compute="_get_contact_info")