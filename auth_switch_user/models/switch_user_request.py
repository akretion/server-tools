# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.http import request


class SwitchUserRequest(models.Model):
    _name = 'switch.user.request'
    _description = 'Switch User Request'

    from_user_id = fields.Many2one(
        'res.users',
        'From User')
    to_user_id = fields.Many2one(
        'res.users',
        'To User')

    @api.multi
    def switch(self):
        request.session['uid'] = self.to_user_id.id
        request.session['login'] = self.to_user_id.login
        context = request.session['context']
        if 'uid' in context:
            context['uid'] = self.to_user_id.id
