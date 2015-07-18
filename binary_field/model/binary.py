# -*- coding: utf-8 -*-
###############################################################################
#
#   Module for OpenERP
#   Copyright (C) 2015 Akretion (http://www.akretion.com).
#   @author Sébastien BEAU <sebastien.beau@akretion.com>
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

import logging
import sys

from openerp import models, fields, api
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class StorageBinary(models.Model):
    _name = 'storage.binary'
    _rec_name = 'url'

    @api.model
    def _get_field(self, record, field_name):
        field_obj = self.env['ir.model.fields']
        field = field_obj.search([
            ('model', '=', record._name),
            ('name', '=', field_name),
            ])
        if not field:
            raise UserError(
                _('The field %s with do not exist on the model %s')
                % (field_name, record._name))
        return field

    @api.model
    def _get_storage(self, field):
        storage = field.storage_id
        if not storage:
            storage = self.env['storage.config'].search([
                ('is_default', '=', True),
                ])
            if not storage:
                raise UserError(
                    _('There is not default storage configuration, '
                      'please add one'))
        return storage

    @api.model
    def _get_storage_adapter(self, field):
        storage = self._get_storage(field)
        return storage.get_adapter(field)

    @api.model
    def _process_binary(self, record, field_name, vals):
        _logger.debug('Add binary to model: %s, field: %s'
                      % (record._model, field_name))
        value = vals[field_name]
        file_size = sys.getsizeof(value.decode('base64'))
        field = self._get_field(record, field_name)
        adapter = self._get_storage_adapter(field)
        uid = adapter.add(value)
        return {
            'uid': uid,
            'size': file_size,
            'storage_id': adapter.storage.id,
            'field_id': field.id,
            'is_cache': adapter.is_cache,
            }

    @api.model
    def add(self, records, field_name, vals):
        for record in records:
            if record[field_name]:
                record[field_name].sudo().write({'obsolete': True})
        if not vals[field_name]:
            return None
        else:
            binary_vals = self._process_binary(record, field_name, vals)
            return self.create(binary_vals).id

    @api.depends('uid', 'storage_id')
    @api.one
    def _get_url(self):
        return self._get_storage_adapter(self.field_id).get_url(self.uid)

    @api.depends('uid', 'storage_id')
    @api.one
    def _get_path(self):
        return self._get_storage_adapter(self.field_id).get_path(self.uid)

    @api.depends('uid', 'storage_id')
    @api.one
    def _get_file(self):
        return self._get_storage_adapter().get(self)

    data = fields.Binary(compute='_get_file')
    size = fields.Float()
    path = fields.Char(compute='_get_path', store=True)
    url = fields.Char(compute='_get_url', store=True)
    uid = fields.Char()
    is_cache = fields.Boolean()
    obsolete = fields.Binary(default=False)
    storage_id = fields.Many2one('storage.config')
    field_id = fields.Many2one('ir.model.fields')
