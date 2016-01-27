# coding: utf-8
# © 2015 @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api, _
from openerp.exceptions import Warning as UserError
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime, timedelta


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    @api.model
    def _get_date(self, start_date, delay, resource_id=False):
        """This method gives the first date after a delay from the start date
            considering the working time attached to the company calendar.
        """
        if isinstance(start_date, str):
            start_date = fields.Date.from_string(start_date)
        if not self.id:
            self = self._update_self()
        dt_leave = self.get_leave_intervals(
            resource_id, start_datetime=None, end_datetime=None)
        worked_days = (
            [day['dayofweek'] for day in self.attendance_ids])
        if delay < 0:
            delta = -1
        else:
            delta = 1
        while datetime.strftime(
            start_date, DEFAULT_SERVER_DATE_FORMAT) in dt_leave or str(
                start_date.weekday()) not in worked_days:
            start_date = start_date + timedelta(days=delta)
        date = start_date
        while delay:
            date = date + timedelta(days=delta)
            if datetime.strftime(
                date, DEFAULT_SERVER_DATE_FORMAT) not in dt_leave and str(
                    date.weekday()) in worked_days:
                delay = delay - delta
        return date

    @api.model
    def _update_self(self):
        if not self._context:
            raise UserError(_(
                "Impossible to guess the calendar to use\n"
                "'context' variable is empty.\n"
                "Developer tip: Consider to use inspect lib to get back "
                "the context in ResourceCalendar._get_date()"))
        model = self._context['params']['model']
        obj_id = self._context['params']['id']
        obj = self.env[model].browse(obj_id)
        if 'company_id' in obj._fields.keys():
            company = obj.company_id
        elif self._uid:
            company = self.env['res.users'].browse(self._uid).company_id
        self = company.calendar_id
        if not self:
            raise UserError(_(
                'You need to define a calendar for the company !'))
        return self
