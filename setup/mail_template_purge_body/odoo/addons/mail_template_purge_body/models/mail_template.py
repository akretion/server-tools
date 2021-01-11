# Copyright 2020 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MailTemplate(models.Model):
    _inherit = "mail.template"

    purge_body_after_send = fields.Boolean()

    def send_mail(self, res_id, force_send=False, raise_exception=False, email_values=None, notif_layout=False):
        mail_id = super().send_mail(res_id, force_send, raise_exception, email_values, notif_layout)
        if self.purge_body_after_send:
            self.env["mail.mail"].browse(mail_id).body_html = ""
