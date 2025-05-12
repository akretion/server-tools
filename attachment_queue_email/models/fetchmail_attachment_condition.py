# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FetchmailAttachmentCondition(models.Model):
    _name = "fetchmail.attachment.condition"
    _description = "Fetchmail Attachment Conditions"

    def company_default_get(self):
        company_id = self.env["res.company"]._company_default_get("fetchmail.server")
        return self.env["res.company"].browse(company_id).id

    name = fields.Char(
        string="Condition Name",
        required=True,
    )
    email_from = fields.Char(
        string="Email From",
        help="If empty, catches the emails from every senders.\n"
        "Otherwise catches the emails where the sender's email contains the given "
        "characters",
    )
    email_subject = fields.Char(
        string="Email Subject",
        help="If empty, catches the emails with every kind of Subjects.\n"
        "Otherwise catches the emails where the Subject contains the given characters",
    )
    file_extension = fields.Char(
        string="File Extension",
        help="The extension (or part of the name) of the sought files. "
        "If empty, all the email's attachments will be imported.",
    )
    server_id = fields.Many2one("fetchmail.server", string="Server Mail")
    file_type = fields.Selection(
        selection=[],
        help="The 'file type' is transmited to the 'Attachment Queue' objects created "
        "from the selected emails attachments.\nIt will allow Odoo to recognize "
        "what do do with them once created.",
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
