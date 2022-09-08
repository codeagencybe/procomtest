# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning

class Subscription(models.Model):
    
    _inherit = 'sale.subscription'

    helpdesk_tag_ids = fields.Many2many("helpdesk.tag", string="Ticket Tags")

class SubscriptionTemplate(models.Model):
    
    _inherit = 'sale.subscription.template'

    helpdesk_tag_ids = fields.Many2many("helpdesk.tag", string="Ticket Tags")    

class Helpdesk(models.Model):
    
    _inherit = 'helpdesk.ticket'

    @api.model
    def create(self, vals):
        """
        """
        res = super(Helpdesk, self).create(vals)
        if res.partner_id:
            progress_stage_id = self.env.ref('sale_subscription.sale_subscription_stage_in_progress')
            if res.partner_id.parent_id:
                subscriptions = self.env['sale.subscription'].sudo().search([('partner_id','=', res.partner_id.parent_id.id), ('stage_id','=',progress_stage_id.id)])
            else:
                subscriptions = self.env['sale.subscription'].sudo().search([('partner_id','=', res.partner_id.id), ('stage_id','=',progress_stage_id.id)])
            tags = res.tag_ids.ids
            for subscription in subscriptions:
                for tag in subscription.helpdesk_tag_ids:
                    if tag.id not in tags:
                        tags.append(tag.id)

            if not subscriptions:
                billable_tag = self.env['helpdesk.tag'].sudo().search([('name','in',['billable','Billable'])], limit=1)
                if not billable_tag:
                    billable_tag = self.env['helpdesk.tag'].sudo().create({'name':'Billable'})
                tags.append(billable_tag.id)
            else:
                non_billable_tag = self.env['helpdesk.tag'].sudo().search([('name','in',['non-billable','Non-Billable'])], limit=1)
                if not non_billable_tag:
                    non_billable_tag = self.env['helpdesk.tag'].sudo().create({'name':'Non-Billable'})
                tags.append(non_billable_tag.id)

            res.write({'tag_ids':[(6, 0, list(set(tags)))]})

        return res

class SaleOrder(models.Model):
    
    _inherit = 'sale.order'

    def _prepare_subscription_data(self, template):
        res = super(SaleOrder, self)._prepare_subscription_data(template)
        res['helpdesk_tag_ids'] = [(6, 0, template.helpdesk_tag_ids.ids)]
        return res