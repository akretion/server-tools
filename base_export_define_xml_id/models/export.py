# -*- coding: utf-8 -*-
# Copyright 2018 Akretion
# Copyright Odoo SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ExportMixin(object):

    origin_export_xml_id_func = False

    @staticmethod
    def new_export_xml_id(self):
        return ExportMixin._export_xml_id(self)

    @staticmethod
    def _export_xml_id(self):
        if not self._is_an_ordinary_table():
            raise Exception(
                "You can not export the column ID of model %s, because the "
                "table %s is not an ordinary table."
                % (self._name, self._table))
        ir_model_data = self.sudo().env['ir.model.data']
        data = ir_model_data.search([
            ('model', '=', self._name),
            ('res_id', '=', self.id)
        ])
        if data:
            return ExportMixin.origin_export_xml_id_func(self)
        else:
            if hasattr(self, '_gen_xml_id'):
                name = self._gen_xml_id()
            else:
                name = ExportMixin._gen_xml_id(self)
            ir_model_data.create({
                'model': self._name,
                'res_id': self.id,
                'module': '__export__',
                'name': name,
            })
            return '__export__.%s' % name

    @staticmethod
    def _gen_xml_id(self):
        # Prefix with database uuid
        ir_model_data = self.sudo().env['ir.model.data']
        ir_config = self.env['ir.config_parameter']
        database_uuid = ir_config.get_param('database.uuid')
        postfix = 0
        name = '%s_%s_%s' % (database_uuid, self._table, self.id)
        while ir_model_data.search(
            [('module', '=', '__export__'), ('name', '=', name)]
        ):
            postfix += 1
            name = '%s_%s_%s' % (self._table, self.id, postfix)
        return name


# Monkey patch
ExportMixin.origin_export_xml_id_func = (
    models.BaseModel._BaseModel__export_xml_id)
models.BaseModel._BaseModel__export_xml_id = ExportMixin.new_export_xml_id
