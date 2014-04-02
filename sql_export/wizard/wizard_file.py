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

from openerp.osv.orm import Model
from openerp.osv import fields, orm
from openerp.tools.translate import _


class SqlFileWizard(orm.TransientModel):

    _name = "sql.file.wizard"

    _description = "Allow to the user to save the file with sql request's data"


    _columns = {
        'file': fields.binary('File', required=True, readonly=True),
        'file_name': fields.char('File Name', readonly=True),
    }



