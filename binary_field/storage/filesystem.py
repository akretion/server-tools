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

from abstract import Storage
import hashlib
import os
import logging

_logger = logging.getLogger(__name__)


class FileSystemStorage(Storage):

    def get_path(self, uid):
        path = self._get_base_path()
        return os.path.join(path, uid)

    def _get_base_path(self):
        path = []
        if self.base_path:
            path.append(self.base_path)
        path.append(self.dbname)
        if self.split_cache and self.is_cache:
            path.append('cache')
        else:
            path.append('binary')
        if self.store_by_field:
            path += [self.model_name, self.field_name]
        return os.path.join(*path)

    def _get_uid(self, data):
        sha = hashlib.sha1(data).hexdigest()
        return os.path.join(sha[:2], sha)

    def add(self, value):
        data = value.decode('base64')
        uid = self._get_uid(data)
        path = self.get_path(uid)
        print path
        if not os.path.exists(path):
            try:
                dirname = os.path.dirname(path)
                if not os.path.isdir(dirname):
                    os.makedirs(dirname)
                with open(path, 'wb') as fp:
                    fp.write(data)
            except IOError:
                _logger.error("_file_write writing %s", path)
        return uid

    def get_url(self, uid):
        return os.path.join(
            self.base_external_url,
            self.get_path(uid))

    def get(self, uid):
        path = self.get_path(uid)
        try:
            return open(path, 'rb').read().encode('base64')
        except IOError:
            _logger.error("failed to read %s", path)

    def remove(self, uid):
        path = self.get_path(uid)
        try:
            os.unlink(path)
        except OSError:
            _logger.error("remove could not unlink %s", path)
        except IOError:
            # Harmless and needed for race conditions
            _logger.error("remove could not unlink %s", path)
