# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import json

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    old_storages = env["storage.backend"].search([("id", "!=", 1)])
    protocol_mapping = {
        "ftp": "ftp",
        "sftp": "sftp",
        "filesystem": "file",
    }
    old2new = {}
    all_codes = []
    for old_storage in old_storages:
        options = {}
        if old_storage.backend_type == "ftp":
            options = {
                "host": old_storage.ftp_server,
                "port": old_storage.ftp_port,
                "username": old_storage.ftp_login,
                "password": old_storage.ftp_password,
            }
        elif old_storage.backend_type == "sftp":
            options = {
                "host": old_storage.sftp_server,
                "port": old_storage.sftp_port,
                "username": old_storage.sftp_login,
                "password": old_storage.sftp_password,
            }
        code = old_storage.name[0:3]
        if code in all_codes:
            code = str(old_storage.id)
        all_codes.append(code)
        vals = {
            "name": old_storage.name,
            "code": code.upper(),
            "protocol": protocol_mapping.get(old_storage.backend_type),
            "directory_path": old_storage.directory_path,
            "options": json.dumps(options),
        }
        fs_storage = env["fs.storage"].create(vals)
        old2new[old_storage.id] = fs_storage.id
    cr.execute("SELECT id, old_storage_id FROM attachment_synchronize_task")
    task_id2old_storage_id = cr.fetchall()
    for (task_id, old_storage_id) in task_id2old_storage_id:
        if not old_storage_id:
            continue
        env["attachment.synchronize.task"].browse(task_id).write(
            {"backend_id": old2new[old_storage_id]}
        )

    # custom fields
    cr.execute("SELECT id, storage_geodis_id FROM delivery_carrier_agency")
    for agency_id, old_storage_id in cr.fetchall():
        if not old_storage_id:
            continue
        new_id = old2new[old_storage_id]
        cr.execute(
            "UPDATE delivery_carrier_agency SET storage_geodis_id = %s WHERE id = %s",
            (new_id, agency_id),
        )

    cr.execute("SELECT id, edi_storage_backend_id FROM edi_transport_config")
    for config_id, old_storage_id in cr.fetchall():
        if not old_storage_id:
            continue
        new_id = old2new[old_storage_id]
        cr.execute(
            "UPDATE edi_transport_config SET edi_storage_backend_id = %s WHERE id = %s",
            (new_id, config_id),
        )
