# -*- coding: utf-8 -*-
###############################################################################
#
#   Module for OpenERP
#   Copyright (C) 2014 Akretion (http://www.akretion.com).
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

from ..storage.filesystem import FileSystemStorage
from openerp import fields, models, api


class StorageConfig(models.Model):
    _name = 'storage.config'
    _description = 'Storage Configuration'

    @api.model
    def _get_storage_class(self):
        return {
            'filesystem': {
                'class': FileSystemStorage,
                'name': 'FileSystem',
            }
        }

    @api.model
    def _get_storage_type(self):
        res = []
        for key, vals in self._get_storage_class().items():
            res.append((key, vals['name']))
        return res

    @api.multi
    def get_adapter(self, field):
        self.ensure_one()
        return self._get_storage_class()[self.type]['class'](self, field)

    @api.one
    def _remove_default(self):
        storage = self.search([('is_default', '=', True)])
        if storage != self:
            storage.write({'is_default': False})

    @api.model
    def create(self, vals):
        if vals.get('is_default'):
            self._remove_default()
        return super(StorageConfig, self).create(vals)

    @api.one
    def write(self, vals):
        if vals.get('is_default'):
            self._remove_default()
        return super(StorageConfig, self).write(vals)

    name = fields.Char('Name')
    type = fields.Selection(_get_storage_type)
    base_path = fields.Char()
    is_default = fields.Boolean(help=(
        'Tic that box in order to select '
        'the default storage configuration'))
    store_by_field = fields.Boolean(help=(
        'Tic that box in order to store binary per model and field. '
        'This meant that the path of the storage will be the following'
        'base_path/model_name/field_name/my_image'))
    split_cache = fields.Boolean(help=(
        'Tic that box in order to store the cache (image resize) in '
        'a the directory "cache" instead of "binary"'))
    external_storage_server = fields.Boolean(help=(
        'Tic that box if you want to server the file with an '
        'external server. For example, if you choose the storage '
        'on File system, the binary file can be serve directly with '
        'nginx or apache...'))
    base_external_url = fields.Char(help=(
        'When you use an external server for storing the binary '
        'you have to enter the base of the url where the binary can '
        'be accesible.'))
