# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tools import config

from .common import setup_exporter


def setup_otlp_http_exporter():
    try:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )
        from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
            OTLPMetricExporter,
        )
    except ImportError:
        raise ImportError(
            "Please install opentelemetry-exporter-otlp-proto-http to use the "
            "OTLP exporter"
        )

    otlp_endpoint = config.get(
        "open_telemetry_exporter_endpoint", "http://localhost:4318"
    ).rstrip("/")

    setup_exporter(
        OTLPSpanExporter(endpoint=f"{otlp_endpoint}/v1/traces"),
        OTLPMetricExporter(endpoint=f"{otlp_endpoint}/v1/metrics"),
    )
