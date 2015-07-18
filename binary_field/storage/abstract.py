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

import logging

_logger = logging.getLogger(__name__)


class Storage(object):

    def __init__(self, storage, field):
        self.storage = storage
        self.field = field
        self.base_path = storage.base_path or ''
        self.base_external_url = storage.base_external_url or ''
        self.dbname = storage._cr.dbname
        self.store_by_field = storage.store_by_field
        self.split_cache = storage.split_cache
        self.field_name = field.name
        self.model_name = field.model_id.model
        self.is_cache = field.env[self.model_name]\
            ._fields[self.field_name].is_cache
