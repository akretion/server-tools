# coding: utf-8
# © 2015 @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    calendar_id = fields.Many2one('resource.calendar',
                                  string='Company Working time')
