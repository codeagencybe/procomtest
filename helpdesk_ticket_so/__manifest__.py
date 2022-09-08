# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Ticket from SO",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    "author": "Code Agency",
    "website": "https://codeagency.be",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['so_task_ticket'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
