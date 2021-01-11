# Copyright 2020 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Mail suspend auto delete",
    "version": "14.0.1.0.0",
    "category": "Generic Modules",
    "summary": """ Delete emails flagged "auto_delete" only when specifically
    intended """,
    "author": "Akretion,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/server-tools",
    "depends": ["mail"],
    "license": "AGPL-3",
    "data": [
        "data/data.xml",
    ],
    "installable": True,
}
