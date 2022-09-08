###################################################################################
# 
#    Copyright (C) Cetmix OÜ
#
#   Odoo Proprietary License v1.0
# 
#   This software and associated files (the "Software") may only be used (executed,
#   modified, executed after modifications) if you have purchased a valid license
#   from the authors, typically via Odoo Apps, or if you have received a written
#   agreement from the authors of the Software (see the COPYRIGHT file).
# 
#   You may develop Odoo modules that use the Software as a library (typically
#   by depending on it, importing it and using its resources), but without copying
#   any source code or material from the Software. You may distribute those
#   modules under the license of your choice, provided that this license is
#   compatible with the terms of the Odoo Proprietary License (For example:
#   LGPL, MIT, or proprietary licenses similar to this one).
# 
#   It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#   or modified copies of the Software.
# 
#   The above copyright notice and this permission notice must be included in all
#   copies or substantial portions of the Software.
# 
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#   ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#
###################################################################################

from odoo import api, fields, models


###################
# From for Models #
###################
class EmailFrom(models.Model):
    _name = "cx.email.from"

    name = fields.Char(
        string="Email Address",
        required=True,
        help="Email address including domain (eg 'mail@example.com')",
    )
    model_id = fields.Many2one(
        string="Model",
        required=True,
        comodel_name="ir.model",
        index=True,
        ondelete="cascade",
    )
    override_templates = fields.Boolean(
        string="Replace for Templates",
        help="Replace 'from' even if set explicitly in Mail Template",
    )
    use_for_reply = fields.Boolean(
        string="Use for 'Reply-To'", help="Use address for 'Reply-to' email field"
    )
    _sql_constraints = [
        (
            "model_unique",
            "UNIQUE(model_id)",
            "'From' address for this model already exists!",
        )
    ]


################
# Mail.Message #
################
class MailMessage(models.Model):
    _inherit = "mail.message"

    # -- Create
    @api.model
    def create(self, values):
        # Proceed only if Author is an internal user
        author_id = values.get("author_id", False)
        if author_id:
            users = self.env["res.partner"].browse(author_id).user_ids
            if users and users[0].has_group("base.group_user"):
                # If model is not specified or From is already set
                # (eg via template) fallback
                model_name = values.get("model", False)
                if not model_name:
                    return super(MailMessage, self).create(values)

                # 1. Check if a specific email address for this model is defined
                model = self.env["ir.model"].sudo().search([("model", "=", model_name)])
                if not model:
                    return super(MailMessage, self).create(values)

                model_email = (
                    self.env["cx.email.from"]
                    .sudo()
                    .search([("model_id", "=", model.id)], limit=1)
                )
                if not model_email:
                    return super(MailMessage, self).create(values)

                # 2. Check if email is composed using template
                # with "Email From" set explicitly
                if not model_email.override_templates and self._context.get(
                    "default_use_template", False
                ):
                    return super(MailMessage, self).create(values)

                # 3. Update values. Set 'email_from' based on model settings
                values.update(
                    {
                        "email_from": self.with_context(
                            force_email_from=True
                        )._get_default_from(users[0], model_email.name)
                    }
                )

        # Use context value to force basic version to skip
        return super(MailMessage, self.with_context(default_use_template=True)).create(
            values
        )
