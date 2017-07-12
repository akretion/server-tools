# -*- coding: utf-8 -*-
#  licence AGPL version 3 or later
#  see licence in __openerp__.py or http://www.gnu.org/licenses/agpl-3.0.txt
#  Copyright (C) 2017 Akretion (http://www.akretion.com).
from openerp import api, fields, models


class IrCron(models.Model):
    _inherit = 'ir.cron'

    history_ids = fields.One2many(
        'ir.cron.history', 'cron_id',
        'Cron Time Historic', readonly=True,
    )
    log_history = fields.Boolean()

    @api.model
    def _callback(self, model_name, method_name, args, job_id):
        date_start = fields.Datetime.now()
        super(IrCron, self)._callback(model_name, method_name, args, job_id)
        cron = self.browse(job_id)
        if cron.log_history:
            date_end = fields.Datetime.now()
            vals = {
                'cron_id': job_id,
                'date_start': date_start,
                'date_end': date_end,
            }
            self.env['ir.cron.history'].create(vals)
