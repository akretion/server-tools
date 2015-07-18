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

from openerp import SUPERUSER_ID
from abtract import Storage
import hashlib
import os
import sys
import logging

_logger = logging.getLogger(__name__)


class FileSystemStorage(Storage):

    def _full_path(self, cr, uid, fname):
        return os.path.join(
            self.config['base_path'],
            self.cr.dbname,
            '%s-%s' % (self.model_name, self.field_name),
            fname)

    # Code extracted from Odoo V8 in ir_attachment.py
    # Copyright (C) 2004-2014 OPENERP SA
    # Licence AGPL V3
    def _get_path(self, cr, uid, bin_data):
        sha = hashlib.sha1(bin_data).hexdigest()
        # scatter files across 256 dirs
        # we use '/' in the db (even on windows)
        fname = sha[:2] + '/' + sha
        full_path = self._full_path(cr, uid, fname)
        dirname = os.path.dirname(full_path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        return fname, full_path

    def _file_read(self, cr, uid, fname, bin_size=False):
        full_path = self._full_path(cr, uid, fname)
        r = ''
        try:
            if bin_size:
                r = os.path.getsize(full_path)
            else:
                r = open(full_path, 'rb').read().encode('base64')
        except IOError:
            _logger.error("_read_file reading %s", full_path)
        return r

    def _file_write(self, cr, uid, value):
        bin_value = value.decode('base64')
        fname, full_path = self._get_path(cr, uid, bin_value)
        if not os.path.exists(full_path):
            try:
                with open(full_path, 'wb') as fp:
                    fp.write(bin_value)
            except IOError:
                _logger.error("_file_write writing %s", full_path)
        return fname

    def _file_delete(self, cr, uid, fname):
        obj = self.pool[self.model_name]
        count = obj.search(cr, 1, [
            ('%s_uid' % self.field_name, '=', fname),
            ], count=True)
        full_path = self._full_path(cr, uid, fname)
        if count <= 1 and os.path.exists(full_path):
            try:
                os.unlink(full_path)
            except OSError:
                _logger.error("_file_delete could not unlink %s", full_path)
            except IOError:
                # Harmless and needed for race conditions
                _logger.error("_file_delete could not unlink %s", full_path)
    # END of extraction

    def add(self, value):
        if not value:
            return {}
        file_size = sys.getsizeof(value.decode('base64'))
        _logger.debug('Add binary to model: %s, field: %s'
                      % (self.model_name, self.field_name))
        binary_uid = self._file_write(self.cr, SUPERUSER_ID, value)
        return {
            'binary_uid': binary_uid,
            'file_size': file_size,
            }

    def update(self, binary_uid, value):
        _logger.debug('Delete binary model: %s, field: %s, uid: %s'
                      % (self.model_name, self.field_name, binary_uid))
        self._file_delete(self.cr, SUPERUSER_ID, binary_uid)
        if not value:
            return {}
        return self.add(value)

    def get(self, binary_uid):
        if not binary_uid:
            return None
        return self._file_read(self.cr, SUPERUSER_ID, binary_uid)

    def get_url(self, binary_uid):
        if not binary_uid:
            return None
        return os.path.join(
            self.config['base_external_url'],
            self.cr.dbname,
            '%s-%s' % (self.model_name, self.field_name),
            binary_uid)
