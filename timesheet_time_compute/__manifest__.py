# -*- coding: utf-8 -*-
{
    'name': "Timesheet Duration Calculation",

    'summary': """
        Duration calculation based on Start Date-Time / End Date-Time""",

    'description': """
        Long description of module's purpose
    """,

    "author": "Code Agency",
    "website": "https://codeagency.be",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['hr_timesheet', 'project', 'helpdesk_sale_timesheet'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
}
