# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Invoice(models.Model):
    
    _inherit = 'account.move'

    def action_post(self):
        res = super(Invoice, self).action_post()
        partner_company_id = self.partner_id.parent_id
        existing_follower_partner_ids = [x.partner_id.id for x in self.message_follower_ids]
        for partner in partner_company_id.child_ids:
            if partner.send_invoice_copy and partner.id != self.partner_id.id and partner.id not in existing_follower_partner_ids:
                self.add_followers(self.id, self._name, partner.id)
        return res

    def add_followers(self, res_id, model, partner_id):
        follower_id = False
        reg = {
            'res_id': res_id,
            'res_model': model,
            'partner_id': partner_id,
            'subtype_ids':[(4, self.env.ref("mail.mt_comment").id)]
        }
        try:
            follower_id = self.env['mail.followers'].create(reg)
        except:
            # This partner is already following this record
            return False
        return follower_id

class Partner(models.Model):
    
    _inherit = 'res.partner'

    send_invoice_copy = fields.Boolean("Send Invoice Copy?", default=False)

    def action_check_invoice_copy_status(self):
        """
        """
        self.send_invoice_copy = True

    def action_uncheck_invoice_copy_status(self):
        """
        """
        self.send_invoice_copy = False