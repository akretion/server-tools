# Copyright 2020 Akretion (http://www.akretion.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.pattern_import_export_xlsx.tests.test_pattern_import import (
    TestPatternImportExcel,
)
from .common import SyncPattimpexCommon


class TestImport(SyncPattimpexCommon, TestPatternImportExcel):
    def test_import_end_to_end(self):
        pass
