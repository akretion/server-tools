# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def instrument_threading():
    try:
        from opentelemetry.instrumentation.threading import ThreadingInstrumentor
    except ImportError:
        raise ImportError(
            "Please install opentelemetry-instrumentation-threading to use the "
            "Threading instrumentation"
        )

    ThreadingInstrumentor().instrument()
