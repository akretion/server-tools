# Copyright 2023 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import csv
import datetime
from io import StringIO

from odoo import fields, models


class SynchronizeExportableMixin(models.AbstractModel):
    _name = "synchronize.exportable.mixin"
    export_date = fields.Serialized()
    export_filename = fields.Serialized()
    export_date_processed = fields.Serialized()
    export_flag = fields.Serialized()

    @property
    def _sync_fields(self):
        """Format as in mode:[fields]"""
        return {}

    def write(self, vals):
        fields_changed = list(vals.keys())
        for mode, field_trigger in self._sync_fields.items():
            if field_trigger in fields_changed:
                self.export_flag[mode].update({mode: True})
        return super().write(vals)

    def track_export_date(self, flow):
        self.export_date[flow] = datetime.datetime.now()

    def track_export_filename(self, flow, filename):
        self.export_filename[flow] = filename

    def track_date_processed(self, flow, date):
        self.export_date_processed[flow] = date

    def set_flag_export(self, flow):
        self.export_flag[flow] = True

    def unset_flag_export(self, flow):
        self.export_flag[flow] = False

    def synchronize_export(self, mode, **kwargs):
        data = self._prepare_export_data(mode, **kwargs)
        file, filename = self._format_to_exportfile(mode, data, **kwargs)
        self._postprocess_export(mode, data, file, filename, **kwargs)
        self.track_export_date(mode)
        self.track_export_filename(mode, filename)
        self.unset_flag_export(mode)
        return file, filename

    def _prepare_export_data(self, mode, **kwargs) -> list:
        return getattr(self, "_prepare_export_data_" + mode)(**kwargs)

    def _format_to_exportfile(self, mode, data, **kwargs):
        return getattr(self, "_format_to_exportfile_" + mode)(data, **kwargs)

    def _postprocess_export(self, mode, data, file, filename, **kwargs):
        try:
            return getattr(self, "_postprocess_export_" + mode)(
                data, file, filename, **kwargs
            )
        except AttributeError:
            return

    def _format_export_to_csv(self, data: list, **kwargs):
        csv_file = StringIO()
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        csv_file.seek(0)
        return csv_file
