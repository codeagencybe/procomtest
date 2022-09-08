# -*- coding: utf-8 -*-
{
    'name': "Sales Order Reference",

    'summary': """
        This module is used to add extra functionalities on sale order.""",

    'description': """
       This module is used to add extra functionalities on sale order.
    """,

    'author': "Code Agency",
    'website': "http://codeagency.be",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.1.5',

    # any module necessary for this one to work correctly
    'depends': ['sale'],

    # always loaded
    'data': [
        'views/sale_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
            ],
}
