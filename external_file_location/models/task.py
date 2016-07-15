# coding: utf-8
# @ 2015 Valentin CHEMIERE @ Akretion
#  © @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from .helper import itersubclasses, get_erp_module, is_module_installed
from ..tasks.abstract_fs import AbstractFSTask
from base64 import b64encode


class Task(models.Model):
    _name = 'external.file.task'
    _description = 'External file task'

    name = fields.Char(required=True)

    method = fields.Selection(selection='_get_method', required=True,
                              help='procotol and trasmitting info')

    method_type = fields.Selection(
        [('import', 'Import'), ('export', 'Export')],
        required=True)

    filename = fields.Char(help='File name which is imported.'
                                'You can use file pattern like *.txt'
                                'to import all txt files')
    filepath = fields.Char(help='Path to imported file')

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

    def _get_method(self):
        res = []
        for cls in itersubclasses(AbstractTask):
            if not is_module_installed(self.env, get_erp_module(cls)):
                continue
            if cls._synchronize_type and (
                    'protocol' not in self._context or
                    cls._key == self._context['protocol']):
                cls_info = (cls._key + '_' + cls._synchronize_type,
                            cls._name + ' ' + cls._synchronize_type)
                res.append(cls_info)
        return res

    @api.onchange('method')
    def onchange_method(self):
        if self.method:
            if 'import' in self.method:
                self.method_type = 'import'
            elif 'export' in self.method:
                self.method_type = 'export'

    @api.multi
    def _prepare_attachment_vals(self, abstract_obj, datas):
        self.ensure_one()
        vals = {
            'name': abstract_obj.filename,
            'datas': b64encode(datas),
            'datas_fname': abstract_obj.filename,
            'task_id': self.task.id,
            'external_hash': self.ext_hash,
            'file_type': self.file_type or False,
        }

    @api.model
    def run_task_scheduler(self, domain=None):
        if not domain:
            domain = []
        tasks = self.env['external.file.task'].search(domain)
        for task in tasks:
            if task.method_type == 'export':
                attachment_obj = self.env['ir.attachment.metadata']
                attachments = attachment_obj.search(
                        [('task_id', '=', taks.id), ('state', '!=', 'done')])
                for attachment in attachments:
                    task._run_one_task(attachment)
            else:
                task._run_one_task()
        tasks.run()

    @api.model
    def _get_task_class(self)
        for cls in itersubclasses(AbstractFSTask):
            if not is_module_installed(self.env, get_erp_module(cls)):
                continue
            cls_build = '%s_%s' % (cls._key, cls._synchronize_type)
            if cls._synchronize_type and cls_build == tsk.method:
                method_class = cls
        return method_class

    @api.multi
    def _run_one_task(self, attachment=None):
        self.ensure_one()
        method_class = self._get_task_class()
        config = {
            'host': tsk.location_id.address,
            # ftplib does not support unicode
            'user': tsk.location_id.login and\
            tsk.location_id.login.encode('utf-8'),
            'pwd': tsk.location_id.password and \
            tsk.location_id.password.encode('utf-8'),
            'port': tsk.location_id.port,
            'allow_dir_creation': False,
            'file_name': tsk.filename,
            'path': tsk.filepath,
            'attachment': attachment or None,
            'task': tsk,
            'move_path': tsk.move_path,
            'new_name': tsk.new_name,
            'after_import': tsk.after_import,
            'file_type': tsk.file_type,
            'md5_check': tsk.md5_check,
            }
            conn = method_class(self.env, config)
            conn.run()
