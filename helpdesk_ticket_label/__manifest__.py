# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Enhancements",

    'summary': """
        This module adds label on helpdesk ticket.""",

    'description': """
        This module adds label on helpdesk ticket.
    """,

    "author": "Code Agency",
    "website": "https://codeagency.be",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.1.1',

    # any module necessary for this one to work correctly
    'depends': ['helpdesk', 'helpdesk_sale', 'helpdesk_sale_timesheet'],

    # always loaded
    'data': [
        'data/sequence_data.xml',
        'views/views.xml',
        'report/ticket_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
