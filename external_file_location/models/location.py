# coding: utf-8
# @ 2015 Valentin CHEMIERE @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp.addons.external_file_location.tasks.filestore import FileStoreTask
from openerp.addons.external_file_location.tasks.ftp import FtpTask
from openerp.addons.external_file_location.tasks.sftp import SftpTask


class Location(models.Model):
    _name = 'external.file.location'
    _description = 'Description'

    name = fields.Char(string='Name', required=True)
    protocol = fields.Selection(selection='_get_protocol', required=True)
    address = fields.Char(string='Address', required=True)
    port = fields.Integer()
    login = fields.Char()
    password = fields.Char()
    task_ids = fields.One2many('external.file.task', 'location_id')
    hide_login = fields.Boolean()
    hide_password = fields.Boolean()
    hide_port = fields.Boolean()

    @api.model
    def _get_classes(self):
        "surcharge this method to add new protocols"
        return {
            'ftp': ('FTP', FtpTask),
            'sftp': ('SFTP', SftpTask),
            'file_store': ('File Store', FileStoreTask),
        }

    @api.model
    def _get_protocol(self):
        protocols = self._get_classes()
        selection = []
        for key, val in protocols.iteritems():
            selection.append((key, val[0]))
        return selection

    @api.onchange('protocol')
    def onchange_protocol(self):
        protocols = self._get_classes()
        if self.protocol:
            cls = protocols.get(self.protocol)[1]
            self.port = cls._default_port
            if cls._hide_login:
                self.hide_login = True
            else:
                self.hide_login = False
            if cls._hide_password:
                self.hide_password = True
            else:
                self.hide_password = False
            if cls._hide_port:
                self.hide_port = True
            else:
                self.hide_port = False
