# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'Attachment Queue Account',
    'version': '12.0.1.0.0',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'description': """
            Allow to import bank statement files or account move
            files attachment queue
        """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': [
        'attachment_queue',
        'account_move_base_import'], 
    'data': [ 
        'views/attachment_queue.xml',
    ],
    'installable': True,
}
