from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(IrHttp, self).session_info()
        result['partner_email'] = self.env.user.partner_id.email
        result['partner_phone'] = self.env.user.partner_id.phone or self.env.user.partner_id.mobile
        result['partner_city'] = self.env.user.partner_id.city
        result['partner_country'] = self.env.user.partner_id.country_id.code
        return result