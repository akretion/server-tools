# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def instrument_requests():
    try:
        from opentelemetry.instrumentation.requests import RequestsInstrumentor
    except ImportError:
        raise ImportError(
            "Please install opentelemetry-instrumentation-requests to use the "
            "Requests instrumentation"
        )

    RequestsInstrumentor().instrument()
