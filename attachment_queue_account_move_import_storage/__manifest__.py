# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
{
    "name": "Attachment Queue Account Storage",
    "version": "16.0.1.0.0",
    "author": "Akretion,Odoo Community Association (OCA)",
    "category": "Finance",
    "maintainers": ["florian-dacosta"],
    "complexity": "easy",
    "depends": [
        "attachment_synchronize",
        "attachment_queue_account_move_import",
    ],
    "website": "https://github.com/OCA/server-tools",
    "data": ["views/attachment_synchronize_task.xml"],
    "installable": True,
    "auto_install": True,
    "license": "AGPL-3",
}
