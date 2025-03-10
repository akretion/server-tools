# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tools import config

from ..instrumentations.threading import instrument_threading
from ..instrumentations.psycopg2 import instrument_psycopg2
from ..instrumentations.wsgi import instrument_wsgi
from ..instrumentations.requests import instrument_requests
from ..instrumentations.system_metrics import instrument_system_metrics
from ..exporters.otlp_http import setup_otlp_http_exporter
from ..exporters.otlp_grpc import setup_otlp_grpc_exporter
from ..exporters.debug import setup_debug_exporter


def post_load():
    if not config.get("open_telemetry_enabled", False):
        return

    # Exporter
    exporter = config.get("open_telemetry_exporter", "console")
    if exporter == "otlp-http":
        setup_otlp_http_exporter()
    elif exporter == "otlp-grpc":
        setup_otlp_grpc_exporter()
    elif exporter == "console":
        setup_debug_exporter()

    # Instrumentation
    if config.get("open_telemetry_instrument_threading", False):
        instrument_threading()

    if config.get("open_telemetry_instrument_psycopg2", False):
        instrument_psycopg2()

    if config.get("open_telemetry_instrument_wsgi", True):
        instrument_wsgi()

    if config.get("open_telemetry_instrument_requests", False):
        instrument_requests()

    if config.get("open_telemetry_instrument_system_metrics", False):
        instrument_system_metrics()
