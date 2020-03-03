# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import os

from distutils.util import strtobool

from openerp.tools.config import config

_logger = logging.getLogger(__name__)

try:
    import elasticapm
except ImportError:
    _logger.warning('elasticapm must be installed')
    elasticapm = None  # noqa


def is_true(strval):
    return bool(strtobool(strval or '0'.lower()))


elastic_apm_active = is_true(os.environ.get('ELASTIC_APM'))


if elastic_apm_active and elasticapm:
    elasticapm.instrument()
    elastic_apm_client = elasticapm.Client(
        framework_name="Odoo",
        framework_version="8.0",
        )
