# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'Account Move Statement Metadata',
    'version': '12.0.1.0.0',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'description': """
            Allow to import bank statement files or account move
            files from ir attachment metadata
        """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': [
        'base_attachment_queue',
        'account_move_base_import'], 
    'data': [ 
        'views/attachment_metadata.xml',
    ],
    'installable': True,
}
