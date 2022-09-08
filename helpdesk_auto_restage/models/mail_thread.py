# -*- coding: utf-8 -*-

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _message_create(self, values_list):
        res = super(MailThread, self)._message_create(values_list)
        for mail_message in res:
            if mail_message.model == 'helpdesk.ticket':
                ticket = self.env['helpdesk.ticket'].sudo().search([
                    ('id', '=', mail_message.res_id)])
                stage = self.env['helpdesk.stage'].sudo().search(
                    [('sequence', '=', 0)], limit=1)
                if mail_message.message_type == 'comment' and \
                        ticket.stage_id.id != stage.id:
                    ticket.write({'stage_id': stage.id})
                elif mail_message.message_type == 'email' and \
                        ticket.stage_id.id != stage.id:
                    ticket.write({'stage_id': stage.id})
        return res
