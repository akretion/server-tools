# coding: utf-8
# @ 2016 Florian DA COSTA @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from fs import osfs
import logging
_logger = logging.getLogger(__name__)


class FileStoreTask(osfs.OSFS):

    _key = 'filestore'
    _name = 'File Store'
    _default_port = None
    _hide_login = True
    _hide_password = True
    _hide_port = True

    @staticmethod
    def connect(location):
        conn = osfs.OSFS(location.address)
        return conn
