# -*- coding: utf-8 -*-
{
    'name': "Partner Notes",

    'summary': """
        This module shows notes linked to the partner.""",

    'description': """
        This module shows notes linked to the partner.
    """,

    "author": "Code Agency",
    "website": "https://codeagency.be",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.1.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'note'],

    # always loaded
    'data': [
        'views/note.xml',
        'views/partner.xml',
    ],
}
