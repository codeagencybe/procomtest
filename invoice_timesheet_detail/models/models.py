# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

class Task(models.Model):

    _inherit = 'project.task'


    def convert_ftime_to_clock(self, ftime):
        """
        """
        time_hr , time_min = divmod(ftime, 1)
        time_min *= 60
        time_str = "{}:{}".format(int(time_hr), str(int(time_min)).zfill(2))
        return time_str

    def action_fsm_validate(self):
        """
        """
        res = super(Task, self).action_fsm_validate()
        notes = list()
        order = self.sale_order_id
        timesheet_sol = order.order_line.filtered(lambda sol: sol.qty_delivered_method == 'timesheet')
        
        # Delete Previous Notes
        note_sols = order.order_line.filtered(lambda sol: sol.display_type == 'line_note')
        note_sols.unlink()
        other_sols = order.order_line.filtered(lambda sol:sol.qty_delivered_method != 'timesheet')

        sequence = 1

        if timesheet_sol:
            sequence = timesheet_sol[0].sequence

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

        for o_sol in other_sols:
            sequence += 1
            o_sol.sudo().write({'sequence': sequence})

        return res