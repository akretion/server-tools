# Copyright 2020 Akretion (http://www.akretion.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import openpyxl

from odoo.addons.pattern_import_export_xlsx.tests.test_pattern_export import (
    TestPatternExportExcel,
)
from .common import SyncPattimpexCommon, PATTIMPEX_NAME


class TestExport(SyncPattimpexCommon, TestPatternExportExcel):
    def setUp(self):
        super().setUp()
        self.user = self.env.ref("base.user_admin")

    def test_export_end_to_end(self):
        """
        Test that we get the correct result from the first step to the last one
        with resulting XLSX
        """
        self.task_export.run_export_pattimpex()
        result = self.backend._list("test_export")
        self.assertIn(result[0], [PATTIMPEX_NAME])
        self.assertIn(result[0], [".xlsx"])
        excel_raw = self.backend._get_bin_data("test_export/" + result[0])
        openpyxl.load_workbook(excel_raw)
        expected_vals = [
            [str(self.env.ref("base.user_admin").id), "Mitchell Admin"],
            [str(self.env.ref("base.user_demo").id), "Marc Demo"],
        ]
        self._helper_check_cell_values(expected_vals)
