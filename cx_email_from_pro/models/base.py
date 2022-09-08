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

from odoo import models, tools


class BaseModel(models.AbstractModel):
    _inherit = "base"

    def _notify_get_reply_to(
        self, default=None, records=None, company=None, doc_names=None
    ):
        """
        Cetmix. In Pro version we add an ability to modify 'Reply-to'
        This is a copy-paste of the base method.
         Need to check it regularly for possible changes
        """
        if records:
            raise ValueError(
                "Use of records is deprecated as this method is available on BaseModel."
            )

        _records = self
        model = (
            _records._name if _records and _records._name != "mail.thread" else False
        )
        res_ids = _records.ids if _records and model else []
        _res_ids = res_ids or [False]  # always have a default value located in False

        alias_domain = (
            self.env["ir.config_parameter"].sudo().get_param("mail.catchall.domain")
        )
        result = dict.fromkeys(_res_ids, False)
        result_email = dict()
        doc_names = doc_names if doc_names else dict()

        if alias_domain:
            if model and res_ids:
                if not doc_names:
                    doc_names = {rec.id: rec.display_name for rec in _records}

                mail_aliases = (
                    self.env["mail.alias"]
                    .sudo()
                    .search(
                        [
                            ("alias_parent_model_id.model", "=", model),
                            ("alias_parent_thread_id", "in", res_ids),
                            ("alias_name", "!=", False),
                        ]
                    )
                )
                # take only first found alias for each thread_id,
                # to match order (1 found -> limit=1 for each res_id)
                for alias in mail_aliases:
                    result_email.setdefault(
                        alias.alias_parent_thread_id,
                        "{}@{}".format(alias.alias_name, alias_domain),
                    )

            # Cetmix. Check for model-wide address
            left_ids = set(_res_ids) - set(result_email)
            if model and left_ids:
                model_email = (
                    self.env["cx.email.from"]
                    .sudo()
                    .search(
                        [("model_id.model", "=", model), ("use_for_reply", "=", True)],
                        limit=1,
                    )
                )
                if model_email:
                    result_email.update(
                        {rid: "%s" % model_email.name for rid in left_ids}
                    )

            # left ids: use catchall
            left_ids = set(_res_ids) - set(result_email)
            if left_ids:
                catchall = (
                    self.env["ir.config_parameter"]
                    .sudo()
                    .get_param("mail.catchall.alias")
                )
                if catchall:
                    result_email.update(
                        {
                            rid: "{}@{}".format(catchall, alias_domain)
                            for rid in left_ids
                        }
                    )

            # compute name of reply-to - TDE tocheck: quotes and stuff like that
            # Cetmix
            company_id = company if company else self.env.user.company_id

            # Prepend with user's name
            if company_id.add_sender_reply_to:
                if company_id.email_joint:
                    company_name = " ".join(
                        (self.env.user.name, company_id.email_joint, company_id.name)
                    )
                else:
                    company_name = " ".join((self.env.user.name, company_id.name))
            else:
                company_name = company_id.name

            for res_id in result_email:
                name = "{}{}{}".format(
                    company_name,
                    " " if doc_names.get(res_id) else "",
                    doc_names.get(res_id, ""),
                )
                result[res_id] = tools.formataddr((name, result_email[res_id]))

        left_ids = set(_res_ids) - set(result_email)
        if left_ids:
            result.update({res_id: default for res_id in left_ids})

        return result
