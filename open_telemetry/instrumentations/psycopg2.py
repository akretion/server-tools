# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def instrument_psycopg2():
    try:
        from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
    except ImportError:
        raise ImportError(
            "Please install opentelemetry-instrumentation-psycopg2 to use the "
            "Psycopg2 instrumentation"
        )

    Psycopg2Instrumentor().instrument()
