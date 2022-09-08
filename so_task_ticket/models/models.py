# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

class SaleOrder(models.Model):
    
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        if not vals.get('fiscal_position_id'):
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            vals['fiscal_position_id'] = partner.property_account_position_id.id
        res = super(SaleOrder, self).create(vals)
        return res

    ticket_id = fields.Many2one('helpdesk.ticket', string="Ticket", help="Ticket from which quotation have been created")

class HelpdeskTicket(models.Model):

    _inherit = 'helpdesk.ticket'

    def _get_action_view_so_ids(self):
        return self.sale_order_id.ids

    def action_mark_as_done(self):
        done_stage = self.env['helpdesk.stage'].search([('name','!=', 'Cancelled'), ('is_close', '=', True)], limit=1)
        if done_stage:
            view = self.env.ref('so_task_ticket.view_mark_ticket_done_wizard')
            wiz = self.env['ticket.task.mark.done.wizard'].create({'ticket_id': self.id})
            return {
                'name': _('Mark as Done Wizard'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'ticket.task.mark.done.wizard',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }
        raise _("No Done Stage found for the task.")

    def view_sale_order(self):
        self.ensure_one()
        so_ids = self._get_action_view_so_ids()
        action_window = {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "name": "Sales Order",
            "views": [[False, "tree"], [False, "form"]],
            "context": {"create": False, "show_sale": True},
            "domain": [["id", "in", so_ids]],
        }
        if len(so_ids) == 1:
            action_window["views"] = [[False, "form"]]
            action_window["res_id"] = so_ids[0]

        return action_window

    is_close = fields.Boolean(related="stage_id.is_close")

    def convert_ftime_to_clock(self, ftime):
        """
        """
        time_hr , time_min = divmod(ftime, 1)
        time_min *= 60
        time_str = "{}:{}".format(int(time_hr), str(int(time_min)).zfill(2))
        return time_str

    def create_so_from_ticket(self):
        """
        """
        if not self.team_id.use_helpdesk_sale_timesheet:
            raise Warning(_("Please enable 'Time Reinvoicing' in Helpdesk Team."))

        if self.sale_order_id:
            raise Warning(_("Sale Order already created."))


        if not self.partner_id:
            raise Warning(_("Please select a customer."))
        
        if not self.project_id.timesheet_product_id:
            raise Warning(_("Please select timesheet product in project."))

        order = self.env['sale.order'].create({'partner_id':self.partner_id.id,'ticket_id':self.id,'company_id': self.company_id.id,'payment_term_id':self.partner_id.property_payment_term_id.id,
            'fiscal_position_id':self.partner_id.property_account_position_id.id,})

        # PrePare Order lines
        product_id = self.project_id.timesheet_product_id
        
        sequence = 1
        
        order_line_vals = {
            'order_id':order.id,
            'product_id':product_id.id,
            'is_service': True,
            'product_uom_qty':self.total_hours_spent,
            'qty_delivered':self.total_hours_spent,
            'sequence':sequence,
        }

        
        order_line = self.env['sale.order.line'].create(order_line_vals)
        
        for line in self.timesheet_ids:

            sequence += 1
            timesheet_note = """Uitgevoerd door: {}\t\t\tDatum: {}\t\t\tStart: {}\t\t\tStop: {}\nOmschrijving: {}""".format(
                    line.user_id.name, 
                    line.date.strftime(DEFAULT_SERVER_DATE_FORMAT),
                    self.convert_ftime_to_clock(line.start_time),
                    self.convert_ftime_to_clock(line.end_time),
                    line.name
                )
        
            self.env['sale.order.line'].sudo().create({'order_id':order.id, 'display_type':'line_note', 'sequence':sequence, 'name':timesheet_note })

        order.action_confirm()

        # Self Updatations
        self.write({'sale_order_id':order.id,'sale_line_id':order_line.id})

class ProjectTask(models.Model):

    _inherit = 'project.task'

    @api.depends("project_id")
    def _compute_allow_quotations(self):
        """
        """
        for task in self:
            create_direct_so = True
            if not task.project_id.allow_quotations:
                create_direct_so = False
            task.update({
                    'create_direct_so':create_direct_so,
                })

    create_direct_so = fields.Boolean(compute="_compute_allow_quotations")

    def action_mark_as_done(self):
        done_stage = self.env['project.task.type'].search([('name','!=', 'Cancelled'), ('is_closed', '=', True)], limit=1)
        if done_stage:
            view = self.env.ref('so_task_ticket.view_mark_done_wizard')
            wiz = self.env['ticket.task.mark.done.wizard'].create({'task_id': self.id})
            return {
                'name': _('Mark as Done Wizard'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'ticket.task.mark.done.wizard',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }
        raise _("No Done Stage found for the task.")

    def convert_ftime_to_clock(self, ftime):
        """
        """
        time_hr , time_min = divmod(ftime, 1)
        time_min *= 60
        time_str = "{}:{}".format(int(time_hr), str(int(time_min)).zfill(2))
        return time_str

    def create_so_from_ticket(self):
        """
        """
        if self.sale_order_id:
            raise Warning(_("Sale Order already created."))


        if not self.partner_id:
            raise Warning(_("Please select a customer."))
        
        if not self.project_id.timesheet_product_id:
            raise Warning(_("Please select timesheet product in project."))


        order = self.env['sale.order'].create({'partner_id':self.partner_id.id,'task_id':self.id,'company_id': self.company_id.id,'payment_term_id':self.partner_id.property_payment_term_id.id,
            'fiscal_position_id':self.partner_id.property_account_position_id.id,})

        # PrePare Order lines
        product_id = self.project_id.timesheet_product_id
        
        sequence = 1

        order_line_vals = {
            'order_id':order.id,
            'product_id':product_id.id,
            'is_service': True,
            'product_uom_qty':self.planned_hours,
            'qty_delivered':self.effective_hours,
            'sequence':sequence,
        }

        
        order_line = self.env['sale.order.line'].create(order_line_vals)
        
        for line in self.timesheet_ids:

            sequence += 1
            timesheet_note = """Uitgevoerd door: {}\t\t\tDatum: {}\t\t\tStart: {}\t\t\tStop: {}\nOmschrijving: {}""".format(
                    line.user_id.name, 
                    line.date.strftime(DEFAULT_SERVER_DATE_FORMAT),
                    self.convert_ftime_to_clock(line.start_time),
                    self.convert_ftime_to_clock(line.end_time),
                    line.name
                )
        
            self.env['sale.order.line'].sudo().create({'order_id':order.id, 'display_type':'line_note', 'sequence':sequence, 'name':timesheet_note })


        order.action_confirm()
        # Self Updatations
        self.write({
                'sale_order_id':order.id,
                'sale_line_id':order_line.id
            })

class ActionMarkDone(models.TransientModel):
    
    _name = 'ticket.task.mark.done.wizard'

    task_id = fields.Many2one('project.task', 'Task', required=False)
    ticket_id = fields.Many2one('helpdesk.ticket', 'Ticket', required=False)


    def action_task_create_so_and_done(self):
        task_id = self.task_id
        try:
            task_id.create_so_from_ticket()
            done_stage = self.env['project.task.type'].search([('name','!=', 'Cancelled'), ('is_closed', '=', True)], limit=1)
            if done_stage:
                task_id.write({'stage_id':done_stage.id})
        except UserError as e:
            raise Warning(e)


    def action_task_mark_done(self):
        task_id = self.task_id
        done_stage = self.env['project.task.type'].search([('name','!=', 'Cancelled'), ('is_closed', '=', True)], limit=1)
        if done_stage:
            task_id.write({'stage_id':done_stage.id})
        return


    def action_ticket_create_so_and_done(self):
        ticket_id = self.ticket_id
        try:
            ticket_id.create_so_from_ticket()
            done_stage = self.env['helpdesk.stage'].search([('name','!=', 'Cancelled'), ('is_close', '=', True)], limit=1)
            if done_stage:
                ticket_id.write({'stage_id':done_stage.id})
        except UserError as e:
            raise Warning(e)


    def action_ticket_mark_done(self):
        ticket_id = self.ticket_id
        done_stage = self.env['helpdesk.stage'].search([('name','!=', 'Cancelled'), ('is_close', '=', True)], limit=1)
        if done_stage:
            ticket_id.write({'stage_id':done_stage.id})
        return
