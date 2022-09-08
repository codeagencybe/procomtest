# -*- coding: utf-8 -*-
{
    'name': "Mandatory Assigned To Field Project/Helpdesk",

    'summary': """
        Change assigned to field mandatory""",

    'description': """
        Change assigned to field mandatory
    """,

    "author": "Code Agency",
    "website": "https://codeagency.be",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['helpdesk', 'project'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
}
