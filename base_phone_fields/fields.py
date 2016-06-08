# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import fields, models
from operator import attrgetter


class Phone(fields.Char):

    _slots = {
        'country_field': None,
    }

    def __init__(self, string=None, country_field=None, **kwargs):
        super(Phone, self).__init__(
            string=string, country_field=country_field, **kwargs)

    _related_country_field = property(attrgetter('country_field'))

    def _setup_regular_base(self, model):
        super(Phone, self)._setup_regular_base(model)
        if not self.country_field:
            self.country_field = 'country_id'

    def _setup_regular_full(self, model):
        super(Phone, self)._setup_regular_full(model)
        assert self.country_field in model._fields, \
            "field %s with unknown country_field %r" % (self, self.country_field)

    def convert_to_cache(self, value, record, validate=True):
        res = super(Phone, self).convert_to_cache(
            value, record, validate=validate)
        # Remove last 2 char from read from database
        print 'db value', res
        if res:
            res = res[:-2]
        print 'cache value', res
        return res


def convert_phone_field(value, country):
    return value + country.code


original_write = models.Model.write

def write(self, vals):
    fields_to_convert = []
    for key in vals:
        if isinstance(self._fields[key], Phone):
            fields_to_convert.append(key)
    if fields_to_convert:
        for record in self:
            loc_vals = vals.copy()
            for field in fields_to_convert:
                country_key = self._fields[field].country_field
                if country_key in loc_vals:
                    country = self.env['res.country'].browse(vals[country_key])
                else:
                    country = record[country_key]
                loc_vals[field] = convert_phone_field(loc_vals[field], country)
            original_write(record, loc_vals)
        return True
    else:
        return original_write(self, vals)
models.Model.write = write
