# -*- coding: utf-8 -*-
{
    'name': "Field Service Travel Expense",

    'summary': """
        Calculation of Travel Expense in Sale Order from Field Service Tasks.""",

    'description': """
        Long description of module's purpose
    """,

    "author": "Code Agency",
    "website": "https://codeagency.be",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base_setup', 'project', 'industry_fsm', 'industry_fsm_sale', 'sale_timesheet'],

    'data': [
        'views/views.xml',
    ],
}
