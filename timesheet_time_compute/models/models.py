# -*- coding: utf-8 -*-

import pytz
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class Timesheet(models.Model):
    
    _inherit = 'account.analytic.line'

    start_time = fields.Float("Start Time")
    end_time = fields.Float("End Time")

    @api.onchange("start_time", "end_time")
    def onchange_duration(self):
        timesheet = self
        if timesheet.start_time and timesheet.end_time:
            self.unit_amount = timesheet.end_time - timesheet.start_time

    @api.constrains('name')
    def check_description(self):
        for line in self:
            if line.name == '/' or not line.name:
                raise ValidationError(_("Please enter valid description."))
        return True

class ProjectTaskCreateTimesheet(models.TransientModel):
    _inherit = 'project.task.create.timesheet'

    start_time = fields.Float("Start Time")
    end_time = fields.Float("End Time")

    @api.depends('start_time', 'end_time')
    def compute_time_spent(self):
        for wiz in self:
            time_spent = 0
            if wiz.start_time and wiz.end_time:
                time_spent = wiz.end_time - wiz.start_time
            wiz.update({
                    'time_spent':time_spent,
                })

    time_spent = fields.Float(compute="compute_time_spent")

    # @api.onchange("start_time", "end_time")
    # def onchange_duration(self):
    #     timesheet = self
    #     if timesheet.start_time and timesheet.end_time:
    #         self.time_spent = timesheet.end_time - timesheet.start_time

    def save_timesheet(self):
        values = {
            'task_id': self.task_id.id,
            'project_id': self.task_id.project_id.id,
            'date': fields.Date.context_today(self),
            'name': self.description,
            'user_id': self.env.uid,
            'unit_amount': self.time_spent,
            'start_time':self.start_time,
            'end_time':self.end_time,
        }
        self.task_id.user_timer_id.unlink()
        return self.env['account.analytic.line'].create(values)

class Task(models.Model):
    
    _inherit = 'project.task'

    def convert_to_local_tz(self, dt_obj):
        user_tz = self.env.user.tz
        server_local = pytz.timezone('utc')
        dt_obj_local = server_local.localize(dt_obj, is_dst=None)
        res = dt_obj_local.astimezone(pytz.timezone(user_tz)).replace(tzinfo=None)
        return res

    def _action_open_new_timesheet(self, time_spent):
        start_time = self.convert_to_local_tz(self.timer_start)
        end_time = self.convert_to_local_tz(fields.Datetime.now())
        return {
            "name": _("Confirm Time Spent"),
            "type": 'ir.actions.act_window',
            "res_model": 'project.task.create.timesheet',
            "views": [[False, "form"]],
            "target": 'new',
            "context": {
                **self.env.context,
                'active_id': self.id,
                'active_model': self._name,
                'default_time_spent': (end_time.hour+(end_time.minute/60)) - (start_time.hour + (start_time.minute/60)),
                'default_start_time': (start_time.hour + (start_time.minute/60)),
                'default_end_time': (end_time.hour+(end_time.minute/60)),
            },
        }

class HelpdeskTicketCreateTimesheet(models.TransientModel):
    _inherit = 'helpdesk.ticket.create.timesheet'
    
    start_time = fields.Float("Start Time")
    end_time = fields.Float("End Time")
    @api.depends('start_time', 'end_time')
    def compute_time_spent(self):
        for wiz in self:
            time_spent = 0
            if wiz.start_time and wiz.end_time:
                time_spent = wiz.end_time - wiz.start_time
            wiz.update({
                    'time_spent':time_spent,
                })

    time_spent = fields.Float(compute="compute_time_spent")

    @api.onchange("start_time", "end_time")
    def onchange_time_start_end(self):
        timesheet = self
        if timesheet.start_time and timesheet.end_time:
            self.time_spent = timesheet.end_time - timesheet.start_time

    def action_generate_timesheet(self):
        values = {
            'task_id': self.ticket_id.task_id.id,
            'project_id': self.ticket_id.project_id.id,
            'date': fields.Datetime.now(),
            'name': self.description,
            'user_id': self.env.uid,
            'start_time':self.start_time,
            'end_time':self.end_time,
            'unit_amount': self.time_spent,
        }

        timesheet = self.env['account.analytic.line'].create(values)

        self.ticket_id.write({
            'timer_start': False,
            'timer_pause': False
        })
        self.ticket_id.timesheet_ids = [(4, timesheet.id, None)]
        self.ticket_id.user_timer_id.unlink()
        return timesheet

class HelpdeskTicket(models.Model):
    
    _inherit = 'helpdesk.ticket'

    def convert_to_local_tz(self, dt_obj):
        user_tz = self.env.user.tz
        server_local = pytz.timezone('utc')
        dt_obj_local = server_local.localize(dt_obj, is_dst=None)
        res = dt_obj_local.astimezone(pytz.timezone(user_tz)).replace(tzinfo=None)
        return res

    def _action_open_new_timesheet(self, time_spent):
        start_time = self.convert_to_local_tz(self.timer_start)
        end_time = self.convert_to_local_tz(fields.Datetime.now())
        return {
            "name": _("Confirm Time Spent"),
            "type": 'ir.actions.act_window',
            "res_model": 'helpdesk.ticket.create.timesheet',
            "views": [[False, "form"]],
            "target": 'new',
            "context": {
                **self.env.context,
                'active_id': self.id,
                'active_model': self._name,
                'default_time_spent': time_spent,
                'default_start_time': (start_time.hour + (start_time.minute/60)),
                'default_end_time': (end_time.hour+(end_time.minute/60)),
            },
        }

