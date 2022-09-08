# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.base.models.ir_qweb import IrQWeb
from lxml import etree

import json
from collections import OrderedDict

from lxml import html
from werkzeug import urls

from odoo import api, models, tools
from odoo.http import request
from odoo.modules.module import get_resource_path

from odoo.addons.base.models.qweb import QWeb, Contextifier

class OdooGenericJSLoader(models.Model):
    _name = 'res.js.loader'
    _description = "Generic JS Loader"

    name = fields.Char('Name', required=True)
    snippet = fields.Text("JS Code", required=True, default="<!--Your JS Code here within <script> tag.-->\n<script>\n.\n.\n.\n</script>")
    applicable_to = fields.Selection([('all', 'Both'), ('frontend','Frontend'), ('backend', 'Backend')], "Apply to", required=True, default="all")
    users = fields.Selection([('all', 'All Users'), ('internal', 'Internal Users Only'), ('visitor', 'Visitors Only')], required=True, default='all')
    enabled = fields.Boolean("Active", default=False)
    related_xml_backend_view_id = fields.Many2one('ir.ui.view', "Related Backend XML View")
    related_xml_frontend_view_id = fields.Many2one('ir.ui.view', "Related Frontend XML View")

    def load_changes(self):
        self.sync_template()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_disable(self):
        self.enabled = False
        return self.load_changes()

    def action_enable(self):
        self.enabled = True
        return self.load_changes()

    def unlink(self):
        self.related_xml_backend_view_id.unlink()
        self.related_xml_frontend_view_id.unlink()
        res = super(OdooGenericJSLoader, self).unlink()
        return res

    def sync_template(self):
        related_xml_backend_view_id = self.related_xml_backend_view_id
        related_xml_frontend_view_id = self.related_xml_frontend_view_id
        
        snippet = self.snippet
        # import pdb;pdb.set_trace()
        root = etree.fromstring(self.snippet)
        
        if self.users == 'all':
            root.set('groups','')
            
        elif self.users == 'internal':
            root.set('groups','base.group_user')            

        elif self.users == 'visitor':
            root.set('groups','base.group_portal')

        self.snippet = etree.tostring(root)

        if not related_xml_backend_view_id:
            related_xml_backend_view_id = self.env.ref("odoo_generic_js_loader.assets_backend_sample").copy()
        if not related_xml_frontend_view_id:
            related_xml_frontend_view_id = self.env.ref("odoo_generic_js_loader.assets_frontend_sample").copy()

        related_xml_backend_view_id.arch_db = """<data inherit_id="web.assets_backend">\n<xpath expr="." position="inside">{}</xpath>\n</data>""".format(self.snippet)
        related_xml_frontend_view_id.arch_db = """<data inherit_id="web.assets_backend">\n<xpath expr="." position="inside">{}</xpath>\n</data>""".format(self.snippet)

        related_xml_frontend_view_id.name = "Frontend JS : " + self.name
        related_xml_backend_view_id.name = "Backend JS : " + self.name

        if self.applicable_to == 'frontend' and self.enabled:
            related_xml_backend_view_id.active = False
            related_xml_frontend_view_id.active = True

        elif self.applicable_to == 'backend' and self.enabled:
            related_xml_backend_view_id.active = True
            related_xml_frontend_view_id.active = False

        elif self.applicable_to == 'all' and self.enabled:
            related_xml_backend_view_id.active = True
            related_xml_frontend_view_id.active = True

        elif not self.enabled:
            related_xml_backend_view_id.active = False
            related_xml_frontend_view_id.active = False

        self.related_xml_backend_view_id = related_xml_backend_view_id
        self.related_xml_frontend_view_id = related_xml_frontend_view_id