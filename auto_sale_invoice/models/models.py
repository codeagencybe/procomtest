# -*- coding: utf-8 -*-

import logging
from odoo.exceptions import Warning
from odoo import models, fields, api, _
from odoo.tools.misc import formatLang, format_date, get_lang

_logger = logging.getLogger(__name__)

class SaleInvoice(models.Model):
    _inherit = 'sale.order'

    @api.depends('invoice_ready')
    def _get_invoice_status_ready(self):
        for order in self:
            if order.invoice_ready:
                order.invoice_ready_selection = 'ready'
            else:
                order.invoice_ready_selection = 'not_ready'


    invoice_ready = fields.Boolean("Ready to Invoice", default=False, store=True, readonly=False)
    invoice_ready_selection = fields.Selection([('ready','Ready to Invoice'), ('not_ready', 'Not Ready to Invoice')], default='not_ready', compute="_get_invoice_status_ready")

    def action_invoice_ready(self):
        for order in self:
            if not order.state == 'sale':
                raise Warning(_("Cannot set to 'Ready for Invoicing'. Order is not confirmed."))
            order.invoice_ready = True

    def create_invoice_from_queue(self):
        orders = self.search([('invoice_ready','=',True), ('state','=', 'sale')])
        order_ids = list()
        for order in orders:
            order = order.with_company(order.company_id)
            current_section_vals = None
            down_payments = order.env['sale.order.line']

            invoice_vals = order._prepare_invoice()
            invoiceable_lines = order._get_invoiceable_lines()

            if any(not line.display_type for line in invoiceable_lines):
                order_ids.append(order.id)

        eligible_orders = self.browse(order_ids)
        try:
            invoices = eligible_orders._create_invoices()
            for invoice in invoices:
                invoice.action_post()
                invoice.send_invoice_auto_mail()
            _logger.info(_("\nAutomatic invoice created for - {}".format([order.name for order in orders])))
        except Exception as e:
            _logger.error(_("\nError creating automatic invoice for - {} {}".format([order.name for order in orders], e)))

class AccountInvoice(models.Model):

    _inherit = 'account.move'

    def send_invoice_auto_mail(self):
        """
        Send Email Automatically
        """
        self.ensure_one()
        template = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False)        
        
        lang = False
        if template:
            lang = template._render_lang(self.ids)[self.id]
        if not lang:
            lang = get_lang(self.env).code

        self.with_context(mark_invoice_as_sent=True).message_post_with_template(template.id, composition_mode='comment')
         
        return
        