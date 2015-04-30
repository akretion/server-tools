# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-TODAY Akretion (<http://www.akretion.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Save translation file',
    'version': '0.1',
    'category': 'Tools',
    'description': """
Save translation file
=====================

This module was written for **developpers** to easily generate i18n files (.po and .pot) from the list of modules,
instead of using the native configuration "Export Translation" wizard.

- The i18n subdirectory is created if missing in the module.
- A ".po" file is generated for each installed languages.
- If a ".po" file exists it is **overwritten** (use with caution).

Credits
=======

Akretion

""",
    'author': 'Akretion, Odoo Community Association (OCA)',
    'depends': ['base'],
    'website': 'https://www.akretion.com',
    'data': [
        'save_translation_file_view.xml',
    ],
    'installable': True,
    'active': False,
}
