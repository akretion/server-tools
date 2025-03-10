To use this module, you need to add it to your server wide modules odoo list. You can do
this by adding the following to your odoo configuration file:

```ini
server_wide_modules = open_telemetry,web
```

Then you have to enable the data collection:

```ini
open_telemetry_enabled = True
open_telemetry_service_name = my-odoo-service
```

Configured like this you should see the collected data about wsgi requests in the
console if you start odoo.

Now you can configure the exporter to send the data to an
[opentelemetry collector](https://opentelemetry.io/docs/collector/configuration/). For
example to send the data to a collector running on the same machine you can use the
following configuration:

```ini
open_telemetry_exporter = otlp-http
open_telemetry_exporter_endpoint = http://localhost:4318
```

Finaly you can enable the various available instrumentations that you want as listed
previously.
