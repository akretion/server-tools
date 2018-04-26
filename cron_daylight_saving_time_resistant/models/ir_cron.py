# -*- coding: utf-8 -*-
# © 2018 Akretion - Raphaël Reverdy
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import pytz
from datetime import datetime

from odoo import api, fields, models
from odoo.addons.base.ir.ir_cron import _intervalTypes
_logger = logging.getLogger(__name__)


class IrCron(models.Model):
    _inherit = "ir.cron"

    daylight_saving_time_resistant = fields.Boolean(
        help="Adjust interval to run at the same hour after and before"
        "daylight saving time change. It's used twice a year")

    @classmethod
    def _process_job(cls, job_cr, job, cron_cr):
        """Add or remove the Daylight saving offset when needed."""
        with api.Environment.manage():
            cron = api.Environment(job_cr, job['user_id'], {})[cls._name]
            now = fields.Datetime.context_timestamp(cron, datetime.now())
            nextcall = fields.Datetime.context_timestamp(
                cron, fields.Datetime.from_string(job['nextcall']))
            delta = _intervalTypes[job['interval_type']](
                job['interval_number'])

            if (nextcall + delta) < now:
                before_offset = (nextcall + delta).utcoffset()
                after_offset = now.utcoffset()
            elif nextcall < now:
                before_offset = nextcall.utcoffset()
                after_offset = (nextcall + delta).utcoffset()
            else:
                before_offset = 0
                after_offset = 0

            diff_offset = after_offset - before_offset

            if diff_offset and job['daylight_saving_time_resistant']:
                numbercall = job['numbercall']
                if nextcall < now and numbercall:
                    nextcall -= diff_offset
                    modified_next_call = fields.Datetime.to_string(
                        nextcall.astimezone(pytz.UTC))
                    job['nextcall'] = modified_next_call
        super(IrCron, cls)._process_job(job_cr, job, cron_cr)
