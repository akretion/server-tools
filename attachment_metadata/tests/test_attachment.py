# coding: utf-8
# ©2016 @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from base64 import b64encode
import hashlib

import openerp.tests.common as common


class TestNewSource(common.TransactionCase):
    def setUp(self):
        super(TestNewSource, self).setUp()
        self.model_attachment = self.env['ir.attachment.metadata']

    def test_attachement_hash(self):
        ir_attachment_id1 = self.model_attachment.create({
            'name': 'filename1',
            'datas': b64encode("Test import1"),
            'datas_fname': 'filename1',
            'external_hash': hashlib.md5("Test import1").hexdigest(),
        })
        self.assertEqual(ir_attachment_id1.internal_hash,
                         ir_attachment_id1.external_hash)
        ir_attachment_id2 = self.model_attachment.create({
            'name': 'filename2',
            'datas': b64encode('Test import2'),
            'datas_fname': 'filename2',
        })
        ir_attachment_ids = ir_attachment_id1 | ir_attachment_id2

        ir_attachment_ids.write(
            {
                'datas': b64encode('Test import1'),
            })
        self.assertEqual(ir_attachment_ids[0].internal_hash,
                         ir_attachment_ids[0].internal_hash)
