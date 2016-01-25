# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from lxml import etree

original_fields_view_get = models.Model.fields_view_get

@api.model
def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):  
    res = original_fields_view_get(
        self,
        view_id=view_id,
        view_type=view_type,
        toolbar=toolbar,
        submenu=submenu)
        
    if view_type == 'tree' and 'base_auto_external_id' in self.env.registry._init_modules:
        doc = etree.XML(res['arch'])
        if doc.xpath("//tree") and len(doc.xpath("//field[@name='external_id']")) == 0:
            node = doc.xpath("//tree")[0]
            node.append(etree.Element("field", name="external_id", string="External ID"))
            res['arch'] = etree.tostring(node)
    return res

models.Model.fields_view_get = fields_view_get

original_add_magic_fields = models.Model._add_magic_fields

@api.model
def _add_magic_fields(self):
    if 'base_auto_external_id' in self.env.registry._init_modules:
        name = 'external_id'
        field = fields.Char(compute='_compute_external_id')
        if name not in self._fields:
            self._add_field(name, field)
    return original_add_magic_fields(self)
        

models.Model._add_magic_fields = _add_magic_fields

@api.multi
def _compute_external_id(self):
    for record in self:
        external_id = record.get_external_id()
        record.external_id=external_id[record.id]

models.Model._compute_external_id = _compute_external_id
