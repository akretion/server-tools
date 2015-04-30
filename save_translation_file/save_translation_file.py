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

import os

from openerp import tools
from openerp.osv import orm
from openerp.modules import get_module_path
from openerp.tools.misc import get_iso_codes


class ir_module_module(orm.Model):
    _inherit = 'ir.module.module'

    def button_save_translation(self, cr, uid, ids, context=None):
        context = context or {}

        format_ = 'po'

        for module in self.browse(cr, uid, ids, context=context):

            i18n_path = os.path.join(get_module_path(module.name), 'i18n')
            if not os.path.isdir(i18n_path):
                os.mkdir(i18n_path)

            lang_obj = self.pool['res.lang']
            condition = [('translatable', '=', True)]
            lang_ids = lang_obj.search(cr, uid, condition, context=context)

            files = [('%s.pot' % module.name, False)]
            for lang in lang_obj.browse(cr, uid, lang_ids, context=context):
                iso_code = get_iso_codes(lang.code)
                filename = '%s.%s' % (iso_code, format_)
                files.append((filename, lang.code))

            for filename, lang in files:
                path = os.path.join(i18n_path, filename)
                with open(path, 'w') as buf:
                    tools.trans_export(lang, module.name, buf, format_, cr)

        return True
