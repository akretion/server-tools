# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    api.Environment(cr, SUPERUSER_ID, {})
    # Add fs_storage_id to avoid it to be computed (from task backend id which is linked
    # to storage.backend, at this step
    cr.execute("ALTER TABLE attachment_queue ADD COLUMN fs_storage_id integer;")

    cr.execute(
        "ALTER TABLE attachment_synchronize_task DROP CONSTRAINT attachment_synchronize_task_backend_id_fkey;"
    )
    cr.execute(
        "ALTER TABLE attachment_synchronize_task RENAME COLUMN backend_id TO old_storage_id"
    )
