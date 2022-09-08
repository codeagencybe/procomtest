# -*- coding: utf-8 -*-
{
    'name': "Contacts Notebook",

    'summary': """
        Adds a new tab / notebook to contacts with wysiwyg field
        to store login credentials.""",

    'description': """
        Long description of module's purpose
    """,

    "author": "Code Agency",
    "website": "https://codeagency.be",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'helpdesk_timesheet', 'industry_fsm'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
}
