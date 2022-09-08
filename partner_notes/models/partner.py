# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class Partner(models.Model):
    _inherit = 'res.partner'

    notes_number = fields.Integer(compute='_get_notes_number', string="Number of Notes")

    def search_notes(self):
        partner_lst = [self.id]
        if self.parent_id:
            partner_lst.append(self.parent_id.id)
        if self.child_ids:
            for child in self.child_ids:
                partner_lst.append(child.id)
        # notes = self.env['note.note'].search([('partner_id', 'in', partner_lst)])
        return partner_lst

    def _get_notes_number(self):
        self.notes_number = 0
        partner_lst = self.search_notes()
        for partner in self:
            partner.notes_number = self.env['note.note'].search_count([('partner_id', 'in', partner_lst)])

    def action_open_notes(self):
        self.ensure_one()
        partner_lst = self.search_notes()
        # partner_lst = [self.id]
        # if self.parent_id:
        #     partner_lst.append(self.parent_id.id)
        # if self.child_ids:
        #     for child in self.child_ids:
        #         partner_lst.append(child.id)
        # notes = self.env['note.note'].search([('partner_id', 'in', partner_lst)])
        # if self.company_type == 'company':
        # else:
        notes = self.env['note.note'].search([('partner_id', 'in', partner_lst)])
        return {
            "type": "ir.actions.act_window",
            "res_model": "note.note",
            "views": [[self.env.ref('note.view_note_note_kanban').id, "kanban"],
                      [self.env.ref('note.view_note_note_tree').id, "tree"],
                      [self.env.ref('note.view_note_note_form').id, "form"]
                      ],
            "domain": [["id", "in", notes.ids]],
            "context": {"create": False},
            "name": _("Notes"),
        }
    

