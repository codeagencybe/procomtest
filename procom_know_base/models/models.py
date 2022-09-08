# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class KnowledgeBaseCategory(models.Model):
    
    _name = 'knowledge.base.category'
    _description = "Knowledge Base Category"

    name = fields.Char("Category Name", required=True)


class KnowledgeBaseTags(models.Model):
    
    _name = 'knowledge.base.tags'
    _description = "Knowledge Base Tags"

    name = fields.Char("Tag Name", required=True)
    color = fields.Integer("Color")

class KnowledgeBaseInfo(models.Model):
    
    _name = 'knowledge.base.info'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = "Knowledge Base Question/Answers"

    
    name = fields.Char("Title", required=True)
    answer = fields.Html("Answer", required=True)
    category_id = fields.Many2one("knowledge.base.category", "Category", required=True)
    tag_ids = fields.Many2many("knowledge.base.tags", string="Tags", required=True)

    def link_to_rec(self):
        ctx = self.env.context
        if ctx.get('ticket_id'):
            rec_id = ctx.get('ticket_id')
            rec_model = 'helpdesk.ticket'
            rec = self.env[rec_model].browse(rec_id)
            rec.write({'kb_ids':[(4, self.id)]})

        if ctx.get('task_id'):
            rec_id = ctx.get('task_id')
            rec_model = 'project.task'
            rec = self.env[rec_model].browse(rec_id)
            rec.write({'kb_ids':[(4, self.id)]})

class HeldpeskTicket(models.Model):
    
    _inherit = 'helpdesk.ticket'

    def view_knowledge_base(self):
        view_id = self.env.ref('procom_know_base.action_knowledge_base_info_tree_view_with_btn').id
        form_view_id = self.env.ref('procom_know_base.action_knowledge_base_info_form_view').id
        context = self._context.copy()
        context['ticket_id'] = self.id
        return {
            'name':'Knowledge Base',
            'view_type':'form',
            'view_mode':'tree,form',
            'res_model':'knowledge.base.info',
            'view_id':view_id,
            'views':[(view_id,'tree'), (form_view_id,'form'),],
            'type':'ir.actions.act_window',
            'domain':[],
            'target':'current',
            'context':context,
        }

    def create_knowledge_base(self):
        view_id = self.env.ref('procom_know_base.action_knowledge_base_info_tree_view_with_btn').id
        form_view_id = self.env.ref('procom_know_base.action_knowledge_base_info_form_view').id
        context = self._context.copy()
        context['ticket_id'] = self.id
        return {
            'name':'Knowledge Base',
            'view_type':'form',
            'view_mode':'tree,form',
            'res_model':'knowledge.base.info',
            'view_id':form_view_id,
            'views':[(form_view_id,'form'),(view_id,'tree')],
            'type':'ir.actions.act_window',
            'domain':[],
            'target':'current',
            'context':context,
        }

    kb_ids = fields.Many2many('knowledge.base.info', 'kb_ticket_rel', 'ticket_id', 'kb_id', string='KB Lines', copy=True, auto_join=True)


class ProjectTask(models.Model):
    
    _inherit = 'project.task'

    def view_knowledge_base(self):
        view_id = self.env.ref('procom_know_base.action_knowledge_base_info_tree_view_with_btn').id
        form_view_id = self.env.ref('procom_know_base.action_knowledge_base_info_form_view').id
        context = self._context.copy()
        context['task_id'] = self.id
        return {
            'name':'Knowledge Base',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'knowledge.base.info',
            'view_id':view_id,
            'views':[(view_id,'tree'), (form_view_id,'form'),],
            'type':'ir.actions.act_window',
            'domain':[],
            'target':'current',
            'context':context,
        }

    def create_knowledge_base(self):
        view_id = self.env.ref('procom_know_base.action_knowledge_base_info_tree_view_with_btn').id
        form_view_id = self.env.ref('procom_know_base.action_knowledge_base_info_form_view').id
        context = self._context.copy()
        context['task_id'] = self.id
        return {
            'name':'Knowledge Base',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'knowledge.base.info',
            'view_id':form_view_id,
            'views':[(form_view_id,'form'),(view_id,'tree')],
            'type':'ir.actions.act_window',
            'domain':[],
            'target':'current',
            'context':context,
        }

    kb_ids = fields.Many2many('knowledge.base.info', 'kb_task_rel', 'task_id', 'kb_id', string='KB Lines', copy=True, auto_join=True)