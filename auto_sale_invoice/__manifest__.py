# -*- coding: utf-8 -*-
{
    'name': "Automatic Invoicing",

    'summary': """
        Users can prepare sale orders and when ready, they must click a new custom action button 
        "ready for invoicing". 
        """,

    'description': """
        Long description of module's purpose
    """,

    "author": "Code Agency",
    "website": "https://codeagency.be",

    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['sale', 'account', 'sale_print_status',],
    'data': [
        'data/cron.xml',
        'views/views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
