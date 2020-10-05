# Copyright 2020 Akretion (http://www.akretion.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.pattern_import_export_xlsx.tests.test_pattern_import import (
    TestPatternImportExcel,
)
import base64
from .common import SyncPattimpexCommon, PATTIMPEX_NAME
from os import path
PATH_BASE = path.dirname(__file__)
import datetime


class TestImport(SyncPattimpexCommon, TestPatternImportExcel):

    def _inject_file_to_storage(self, path):
        data = open(PATH_BASE + path, "rb").read()
        relative_path = "test_import" + PATTIMPEX_NAME + datetime.datetime.now() + ".xlsx"
        self.backend._add_bin_data("test_import/")

    def setUp(self):
        super().setUp()
        self._inject_file_to_storage("fixtures/example.users.txt")

    def test_import_end_to_end(self):
        pass
