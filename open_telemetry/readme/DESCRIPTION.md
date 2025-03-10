This module enables several [OpenTelemetry](https://opentelemetry.io/) instrumentations
for Odoo export the data to an OpenTelemetry collector.

## Supported Instrumentations

- odoo web server (WSGI).

  - odoo config: `open_telemetry_instrument_wsgi` (default: `True`)

- Threading (threading).

  - odoo config: `open_telemetry_instrument_threading` (default: `True`)
  - requires `opentelemetry-instrumentation-threading` package to enable

- PostgreSQL database (psycopg2).

  - odoo config: `open_telemetry_instrument_psycopg2` (default: `False`)
  - requires `opentelemetry-instrumentation-psycopg2` package to enable

- Requests (requests).

  - odoo config: `open_telemetry_instrument_requests` (default: `False`)
  - requires `opentelemetry-instrumentation-requests` package to enable

- System metrics.

  - odoo config: `open_telemetry_instrument_system_metrics` (default: `False`)
  - requires `opentelemetry-instrumentation-system-metrics` package to enable

## Supported Exporters

- Console (stdout).

  - odoo config: `open_telemetry_exporter=console` (default)
  - This is mostly for testing.

- OTLP HTTP/Protobuf

  - odoo config: `open_telemetry_exporter=otlp-http`
  - requires `opentelemetry-exporter-otlp-proto-http` package to enable
  - endpoint is set with `open_telemetry_exporter_endpoint` (default:
    `http://localhost:4318`)

- OTLP gRPC/Protobuf

  - odoo config: `open_telemetry_exporter=otlp-grpc`
  - requires `opentelemetry-exporter-otlp-proto-grpc` package to enable
  - endpoint is set with `open_telemetry_exporter_endpoint` (default:
    `http://localhost:4317`)
