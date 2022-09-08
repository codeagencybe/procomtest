# -*- coding: utf-8 -*-
{
    'name': "Sale Order form Project Task / Helpdesk Timesheet",

    'summary': """
        Create Sale Order from Task/Helpdesk Ticket.
        """,

    'description': """
        Long description of module's purpose
    """,

    "author": "Code Agency",
    "website": "https://codeagency.be",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['sale', 'project', 'helpdesk', 'helpdesk_sale_timesheet', 'industry_fsm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}
