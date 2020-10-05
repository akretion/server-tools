# Copyright 2020 Akretion (http://www.akretion.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import mock
import os
from odoo.addons.attachment_synchronize.tests.common import SyncCommon


class SyncPattimpexCommon(SyncCommon):
    def setUp(self):
        super().setUp()
        self.task_import = self.env.ref(
            "attachment_synchronize_pattimpex.export_to_filestore_pattimpex"
        )
        self.task_export = self.env.ref(
            "attachment_synchronize_pattimpex.import_from_filestore_pattimpex"
        )
