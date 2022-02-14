# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
{
    "name": "Attachment Queue Account",
    "version": "14.0.1.0.0",
    "author": "Akretion,Odoo Community Association (OCA)",
    "maintainer": "Akretion",
    "category": "Finance",
    "complexity": "easy",
    "depends": [
        "account_move_base_import",
        "account_statement_import",
        "attachment_queue",
    ],
    "website": "https://github.com/OCA/server-tools",
    "data": ["views/attachment_queue.xml"],
    "installable": True,
    "auto_install": False,
    "license": "AGPL-3",
}
