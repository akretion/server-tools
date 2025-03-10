# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import odoo.http
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware


class OdooOpenTelemetryMiddleware(OpenTelemetryMiddleware):
    """
    Odoo specific middleware to forward custom application attributes to the
    odoo application.
    """

    def __getattr__(self, item):
        return getattr(self.wsgi, item)


def instrument_wsgi():
    odoo.http.root = OdooOpenTelemetryMiddleware(odoo.http.root)
