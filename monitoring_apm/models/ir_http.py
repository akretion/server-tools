# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models
from openerp.http import request
from ..apm_client import elastic_apm_client, elasticapm
from elasticapm.utils import compat, get_url_dict

SKIP_PATH = [
    "/connector/runjob",
    "/longpolling/",
    ]


def get_data_from_request(request):
    httprequest = request.httprequest
    data = {
        "headers": dict(**httprequest.headers),
        "method": httprequest.method,
        "socket": {
            "remote_address": httprequest.remote_addr,
            "encrypted": httprequest.scheme == 'https'
        },
        "url": get_url_dict(httprequest.url)
    }
    # remove Cookie header since the same data is in request["cookies"] as well
    data["headers"].pop("Cookie", None)
    return data


def get_data_from_response(response):
    data = {"status_code": response.status_code}
#    if response.headers:
#        data["headers"] = {
#            key: ";".join(response.headers.getall(key))
#            for key in compat.iterkeys(response.headers)
#        }
    return data


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def _dispatch(self):
        if not elastic_apm_client:
            return super(IrHttp, self)._dispatch()

        path_info = request.httprequest.environ.get('PATH_INFO')
        for path in SKIP_PATH:
            if path_info.startswith(path):
                return super(IrHttp, self)._dispatch()

        name = path_info
        for key in ['model', 'method', 'signal']:
            val = request.params.get(key)
            if val and val not in name:
                name += ' {}: {}'.format(key, val)

        elastic_apm_client.begin_transaction('request')
        response = super(IrHttp, self)._dispatch()
        elasticapm.set_context(lambda: get_data_from_request(request), "request")
        elasticapm.set_context(lambda: get_data_from_response(response), "response")
        elastic_apm_client.end_transaction(name, response.status_code)
        print 'send', name, response.status_code
        return response
