# -*- coding: utf-8 -*-

import requests
from odoo import models, fields, api, _
from odoo.exceptions import Warning


GoogleDistancematrixEndpoint = "https://maps.googleapis.com/maps/api/distancematrix/json"

Error_status = {
    'NOT_FOUND': 'origin and/or destination of this pairing could not be geocoded.',
    'ZERO_RESULTS': 'no route could be found between the origin and destination.',
    'MAX_ROUTE_LENGTH_EXCEEDED': 'requested route is too long and cannot be processed.'
}


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    google_api_key = fields.Char('Google API Key',
        config_parameter='google_api_key',
        help="Add Google API key it will used to caclculate distance in sale helpdesk")

class Project(models.Model):

    _inherit = 'project.project'

    travel_expense_product_id = fields.Many2one('product.product', string="Travel Expense Product")

class Task(models.Model):

    _inherit = 'project.task'

    distance = fields.Float(string='Distance(km)', digits=(16, 1))

    @api.model
    def create(self, vals):
        res = super(Task, self).create(vals)
        res.on_change_partner()
        return res

    @api.onchange('partner_id')
    def on_change_partner(self):
        if self.partner_id:
            desitnation_add = self.partner_id.contact_address
            origins_add = self.env.user.company_id.partner_id.contact_address
            api_key = self.env['ir.config_parameter'].sudo().get_param('google_api_key', '')
            payload = {
                "units": "metric",
                "origins": origins_add,
                "destinations": desitnation_add,
                "key": api_key
            }
            result = requests.get(GoogleDistancematrixEndpoint, params=payload).json()
            if result['status'] != "OK":
                error = result['error_message']
                return {
                    'warning': {
                        'message': error, 'title': _('Warning'),
                    },
                }
            status = result['rows'][0]['elements'][0]['status']
            if status != 'OK':
                error = Error_status[status]
                return {
                    'warning': {
                        'message': error, 'title': _('Warning'),
                    },
                }
            metre = result['rows'][0]['elements'][0]['distance']['value']
            self.distance = metre / 1000
        else:
            self.distance = 0.0


    def update_travel_expense_in_so(self):
        """
        """
        sale_order = self.sale_order_id
        if sale_order:
            travel_expense_product_id = self.project_id.travel_expense_product_id
            if not travel_expense_product_id:
                raise Warning(_('No Travel Expense Product found in Project Configuration.'))

            travel_expense_product_order_line = [order_line for order_line in sale_order.order_line if order_line.product_id.id == travel_expense_product_id.id]
            if travel_expense_product_order_line:
                travel_expense_product_order_line = travel_expense_product_order_line[0]
                travel_expense_product_order_line.write({'product_uom_qty': self.distance * 2, 'qty_delivered':self.distance *2 }) #qty delivered too
            else:
                order_line = self.env['sale.order.line'].create({'product_id':travel_expense_product_id.id, 'product_uom_qty': self.distance * 2, 'qty_delivered':self.distance *2, 'order_id':sale_order.id})
                for line in order_line:
                    if not line.qty_delivered:
                        line.write({'qty_delivered':line.product_uom_qty})
        else:
            raise Warning(_('No Sale Order Found.'))

    def action_fsm_validate(self):
        """
        """
        res = super(Task, self).action_fsm_validate()
        self.update_travel_expense_in_so()
        return res