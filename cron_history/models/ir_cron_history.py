# -*- coding: utf-8 -*-
#  licence AGPL version 3 or later
#  see licence in __openerp__.py or http://www.gnu.org/licenses/agpl-3.0.txt
#  Copyright (C) 2017 Akretion (http://www.akretion.com).
from openerp import api, fields, models
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime
import time


class IrCronHistory(models.Model):
    _name = 'ir.cron.history'
    _description = 'Historic of cron duration'
    _rec_name = 'cron_id'
    _order = 'date_start desc'

    @api.depends('date_start', 'date_end')
    @api.one
    def _get_cron_duration(self):
        date_start = datetime.strptime(
            self.date_start, DEFAULT_SERVER_DATETIME_FORMAT)
        date_end = datetime.strptime(
            self.date_end, DEFAULT_SERVER_DATETIME_FORMAT)
        # Convert to Unix timestamp
        date_start = time.mktime(date_start.timetuple())
        date_end = time.mktime(date_end.timetuple())
        duration_second = date_end - date_start
        duration_minutes = duration_second / 60
        self.duration = round(duration_minutes, 3)

    @api.depends('date_start')
    @api.one
    def get_str_id(self):
        self.id_str = str(self.id)

    cron_id = fields.Many2one('ir.cron', string='Cron')
    date_start = fields.Datetime()
    date_end = fields.Datetime()
    duration = fields.Float(
        compute='_get_cron_duration',
        store=True,
        help="Cron execution duration (in minutes)")
    id_str = fields.Char(compute='get_str_id', store=True)
