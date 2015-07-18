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

from openerp import fields, models
from openerp.tools import image_resize_image
from openerp.tools.translate import _
from openerp import tools


class BinaryField(fields.Many2one):
    type='binary'

    def __init__(self, string=None, **kwargs):
        super(BinaryField, self).__init__(
            comodel_name='binary.binary', string=string, **kwargs)

    def _get_file(self, record):
        import pdb; pdb.set_trace()
        return 'TODO'

    def _set_file(self, record):
        import pdb; pdb.set_trace()
        return 'TODO'

    def setup(self, env):
        self.compute = self._get_file
        self.inverse = self._set_file

    def _fnct_write(self, obj, cr, uid, ids, field_name, value, args,
                    context=None):
        if not isinstance(ids, (list, tuple)):
            ids = [ids]
        storage_obj = obj.pool['storage.configuration']
        for record in obj.browse(cr, uid, ids, context=context):
            storage = storage_obj.get_storage(cr, uid, field_name, record)
            binary_uid = record['%s_uid' % field_name]
            if binary_uid:
                res = storage.update(binary_uid, value)
            else:
                res = storage.add(value)
            vals = self._prepare_binary_meta(
                cr, uid, field_name, res, context=context)
            record.write(vals)
        return True

    def _read_binary(self, storage, record, field_name, binary_uid,
                     context=None):
        # Compatibility with existing binary field
        if context.get(
            'bin_size_%s' % field_name, context.get('bin_size')
        ):
            size = record['%s_file_size' % field_name]
            return tools.human_size(long(size))
        else:
            return storage.get(binary_uid)

    def _fnct_read(self, obj, cr, uid, ids, field_name, args, context=None):
        result = {}
        storage_obj = obj.pool['storage.configuration']
        for record in obj.browse(cr, uid, ids, context=context):
            storage = storage_obj.get_storage(cr, SUPERUSER_ID, field_name, record)
            binary_uid = record['%s_uid' % field_name]
            if binary_uid:
                result[record.id] = self._read_binary(
                    storage, record, field_name, binary_uid, context=context)
            else:
                result[record.id] = None
        return result


class ImageField(BinaryField):

    def __init__(self, string, get_storage=Storage, config=None, 
            resize_based_on=None, height=64, width=64, **kwargs):
        """Init a ImageField field
        :params string: Name of the field
        :type string: str
        :params get_storage: Storage Class for processing the field
                            by default use the Storage on filesystem
        :type get_storage: :py:class`binary_field.Storage'
        :params config: configuration used by the storage class
        :type config: what you want it's depend of the Storage class
                      implementation
        :params resize_based_on: reference field that should be resized
        :type resize_based_on: str
        :params height: height of the image resized
        :type height: integer
        :params width: width of the image resized
        :type width: integer
        """
        super(ImageField, self).__init__(
            string,
            get_storage=get_storage,
            config=config,
            **kwargs)
        self.resize_based_on = resize_based_on
        self.height = height
        self.width = width

    def _fnct_write(self, obj, cr, uid, ids, field_name, value, args,
                    context=None):
        if context is None:
            context = {}
        related_field_name = obj._columns[field_name].resize_based_on

        # If we write an original image in a field with the option resized
        # We have to store the image on the related field and not on the
        # resized image field
        if related_field_name and not context.get('refresh_image_cache'):
            return self._fnct_write(
                obj, cr, uid, ids, related_field_name, value, args,
                context=context)
        else:
            super(ImageField, self)._fnct_write(
                obj, cr, uid, ids, field_name, value, args, context=context)
            
            for name, field in obj._columns.items():
                if isinstance(field, ImageField)\
                   and field.resize_based_on == field_name:
                    field._refresh_cache(
                        obj, cr, uid, ids, name, context=context)
        return True

    def _read_binary(self, storage, record, field_name, binary_uid,
                     context=None):
        if not context.get('bin_size_%s' % field_name)\
             and not context.get('bin_base64_%s' % field_name)\
             and not context.get('bin_base64')\
             and storage.external_storage_server:
            #if context.get('bin_size'):
                # To avoid useless call by default for the image
                # We never return the bin size but the url
                # SO I remove the key in order to avoid the 
                # automatic conversion in the orm
                #context.pop('bin_size')
            return storage.get_url(binary_uid)
        else:
            return super(ImageField, self)._read_binary(
                storage, record, field_name, binary_uid, context=context)

    def _refresh_cache(self, obj, cr, uid, ids, field_name, context=None):
        """Refresh the cache of the small image
        :params ids: list of object id to refresh
        :type ids: list
        :params field_name: Name of the field to refresh the cache
        :type field_name: str
        """
        if context is None:
            context = {}
        if not isinstance(ids, (list, tuple)):
            ids = [ids]
        ctx = context.copy()
        field = obj._columns[field_name]
        ctx['bin_base64_%s' % field.resize_based_on] = True
        for record_id in ids:
            _logger.debug('Refreshing Image Cache from the field %s of object '
                          '%s id : %s' % (field_name, obj._name, record_id))
            record = obj.browse(cr, uid, record_id, context=ctx)
            original_image = record[field.resize_based_on]
            if original_image:
                size = (field.width, field.height)
                resized_image = image_resize_image(original_image, size)
            else:
                resized_image = None
            write_ctx = ctx.copy()
            write_ctx['refresh_image_cache'] = True
            self._fnct_write(obj, cr, uid, [record_id], field_name,
                             resized_image, None, context=write_ctx)


fields.BinaryField = BinaryField
#fields.ImageField = ImageField
