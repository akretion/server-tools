# -*- coding: utf-8 -*-
###############################################################################
#
#   action_server_email for OpenERP
#   Copyright (C) 2013-TODAY Akretion <http://www.akretion.com>.
#   @author Florian DA COSTA <florian.dacosta@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################


{
    'name': 'SQL Export',
    'version': '0.1',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'description': 
    """
    Allow to execute sql query from openerp interface in order to export datas in csv files.
    To edit or create a query, the user have to be in sql_query editor group.
    To execute a query, the user or group of user have to be specified in the sql_export record.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': [
        "base",
    ], 
    'init_xml': [],
    'update_xml': [ 
        'sql_view.xml',
        'wizard/wizard_file_view.xml',
        'security/sql_export_security.xml',
        'security/ir.model.access.csv',
    ],
    'demo_xml': [],
    'installable': True,
}
