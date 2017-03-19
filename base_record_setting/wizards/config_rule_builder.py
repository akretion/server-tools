# coding: utf-8
# © 2017 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# import ast
# from lxml import etree

# from odoo.osv import orm
from odoo import api, fields, models
# from odoo.exceptions import UserError


class ConfigRuleBuilder(models.TransientModel):
    _name = 'config.rule.builder'
    _description = "Configuration Rule Builder"

    name = fields.Char()
    src_model_id = fields.Many2one(
        comodel_name='ir.model', string='Model')
    config_ids = fields.One2many(
        comodel_name='config.rule.line.builder',
        inverse_name='record_setting_rule_id',
        help="")

    @api.model
    def default_get(self, fields):
        active_id = self._context.get('active_id')
        model = self._context.get('active_model')
        origin = self.env[model].browse(active_id)
        if origin:
            return {
                'src_model_id': self.env['ir.model'].search(
                    [('model', '=', origin.implied_model)]).id,
                'name': origin.name,
            }
        return {}


class ConfigRuleLineBuilder(models.TransientModel):
    _name = 'config.rule.line.builder'

    record_setting_rule_id = fields.Many2one(
        comodel_name='config.rule.builder')
    # implied_record_id = fields.Reference(selection='_authorised_models')
    model_id = fields.Many2one(comodel_name='ir.model')
    field_id = fields.Many2one(comodel_name='ir.model.fields')
    value = fields.Char()
    domain = fields.Char()
    readonly = fields.Boolean()

    @api.model
    def _authorised_models(self):
        """ Inherit this method to add more models depending of your
            modules dependencies
        """
        # TODO remove duplicate
        active_id = self._context.get('active_id')
        model = self._context.get('active_model')
        origin = self.env[model].browse(active_id)
        # if origin:
        #     model = self.env['ir.model'].search(
        #         [('model', '=', origin.implied_model)])
        # else:
        models = self.env['ir.model'].search([])
        return [(x.model, x.name) for x in models]
