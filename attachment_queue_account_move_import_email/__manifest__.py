# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
{
    "name": "Attachment Queue Account Move Import Email",
    "version": "16.0.1.0.0",
    "author": "Akretion,Odoo Community Association (OCA)",
    "maintainers": ["florian-dacosta"],
    "category": "Finance",
    "complexity": "easy",
    "depends": [
        "attachment_queue_account_move_import",
        "attachment_queue_email",
    ],
    "website": "https://github.com/OCA/server-tools",
    "data": ["views/fetchmail_attachment_condition_views.xml"],
    "installable": True,
    "auto_install": True,
    "license": "AGPL-3",
}
