# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Open Telemetry",
    "version": "14.0.1.0.0",
    "author": "Akretion, Odoo Community Association (OCA)",
    "summary": "Open Telemetry integration module for Odoo",
    "category": "Tools",
    "depends": [],
    "website": "https://github.com/OCA/server-tools",
    "data": [],
    "external_dependencies": {
        "python": [
            "opentelemetry-api",
            "opentelemetry-sdk",
            "opentelemetry-instrumentation-wsgi",
            # Optional dependencies:
            # "opentelemetry-instrumentation-psycopg2",
            # "opentelemetry-instrumentation-threading",
            # "opentelemetry-instrumentation-requests",
            # "opentelemetry-instrumentation-system-metrics",
            # "opentelemetry-exporter-otlp-proto-http",
            # "opentelemetry-exporter-otlp-proto-grpc",
        ]
    },
    "maintainers": ["paradoxxxzero"],
    "demo": [],
    "installable": True,
    "license": "AGPL-3",
    "post_load": "post_load",
}
