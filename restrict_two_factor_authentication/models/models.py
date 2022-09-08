# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.base.models.res_users import check_identity
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = 'res.users'

    @check_identity
    def totp_enable_wizard(self):
        """
        """
        if self.env.user.has_group('base.group_system'):
            res = super(ResUsers, self).totp_enable_wizard()
            return res
        raise UserError(_("Access Denied"))
