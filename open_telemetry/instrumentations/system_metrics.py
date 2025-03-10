# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def instrument_system_metrics():
    try:
        from opentelemetry.instrumentation.system_metrics import (
            SystemMetricsInstrumentor,
        )
    except ImportError:
        raise ImportError(
            "Please install opentelemetry-instrumentation-system-metrics to use the "
            "SystemMetrics instrumentation"
        )

    SystemMetricsInstrumentor().instrument()
