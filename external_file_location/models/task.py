# coding: utf-8
# @ 2015 Valentin CHEMIERE @ Akretion
#  © @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp import sql_db
from base64 import b64encode
import os
from unidecode import unidecode


class Task(models.Model):
    _name = 'external.file.task'
    _description = 'External file task'

    name = fields.Char(required=True)

    method_type = fields.Selection(
        [('import', 'Import'), ('export', 'Export')],
        required=True)

    filename = fields.Char(help='File name which is imported.'
                                'You can use file pattern like *.txt'
                                'to import all txt files')
    filepath = fields.Char(help='Path to imported/exported file')

    location_id = fields.Many2one('external.file.location', string='Location',
                                  required=True)

    attachment_ids = fields.One2many('ir.attachment.metadata', 'task_id',
                                     string='Attachment')

    move_path = fields.Char(string='Move path',
                            help='Imported File will be moved to this path')

    new_name = fields.Char(string='New name',
                           help='Imported File will be renamed to this name'
                                'Name can use mako template where obj is an '
                                'ir_attachement. template exemple : '
                                '  ${obj.name}-${obj.create_date}.csv')

    md5_check = fields.Boolean(help='Control file integrity after import with'
                               ' a md5 file')

    after_import = fields.Selection(selection='_get_action',
                                    help='Action after import a file')

    file_type = fields.Selection(
        selection=[],
        string="File type",
        help="The file type determines an import method to be used "
             "to parse and transform data before their import in ERP")

    def _get_action(self):
        return [('rename', 'Rename'),
                ('move', 'Move'),
                ('move_rename', 'Move & Rename'),
                ('delete', 'Delete'),
                ]

    @api.multi
    def _prepare_attachment_vals(self, datas, filename):
        self.ensure_one()
        vals = {
            'name': filename,
            'datas': b64encode(unidecode(datas)),
            'datas_fname': filename,
            'task_id': self.id,
#            'external_hash': self.ext_hash,
            'file_type': self.file_type or False,
        }
        return vals

    @api.model
    def run_task_scheduler(self, domain=None):
        if domain is None:
            domain = []
        tasks = self.env['external.file.task'].search(domain)
        for task in tasks:
            if task.method_type == 'import':
                task.run_import()
            elif task.method_type == 'export':
                task.run_export()

    @api.multi
    def run_import(self):
        self.ensure_one()
        protocols = self.env['external.file.location']._get_classes()
        cls = protocols.get(self.location_id.protocol)[1]
        attach_obj = self.env['ir.attachment.metadata']
        with cls.connect(self.location_id) as conn:
            for file_name in conn.listdir(path=self.filepath,
                                          wildcard=self.filename or '',
                                          files_only=True):
                if self.env.context.get('test', False):
                    new_cr = self.env.cr
                else:
                    new_cr = sql_db.db_connect(self.env.cr.dbname).cursor()
                with api.Environment.manage():
                    try:
                        attach_obj = api.Environment(
                            new_cr, self.env.uid,
                            self.env.context)['ir.attachment.metadata']
                        full_path = os.path.join(self.filepath, file_name)
                        file_data = conn.open(full_path)
                        datas = file_data.read()
                        attach_vals = self._prepare_attachment_vals(
                            datas, file_name)
                        attach_obj.create(attach_vals)
                        new_full_path = False
                        if self.after_import == 'rename':
                            new_full_path = os.path.join(
                                self.filepath, self.new_name)
                        elif self.after_import == 'move':
                            new_full_path = os.path.join(
                                self.move_path, file_name)
                        elif self.after_import == 'move_rename':
                            new_full_path = os.path.join(
                                self.move_path, self.new_name)
                        if new_full_path:
                            conn.rename(full_path, new_full_path)
                        if self.after_import == 'delete':
                            conn.remove(full_path)
                    except Exception, e:
                        new_cr.rollback()
                        raise e
                    else:
                        if not self.env.context.get('test', False):
                            new_cr.commit()
                    finally:
                        if not self.env.context.get('test', False):
                            new_cr.close()

    @api.multi
    def run_export(self):
        self.ensure_one()
        attachment_obj = self.env['ir.attachment.metadata']
        attachments = attachment_obj.search(
            [('task_id', '=', self.id), ('state', '!=', 'done')])
        for attachment in attachments:
            attachment.run()
