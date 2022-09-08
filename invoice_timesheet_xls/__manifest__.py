# -*- coding: utf-8 -*-
{
    'name': "Invoice Timesheet XLS",
    'summary': """
        This module helps customers to download Timesheet XLS from portal.
    """,
    'description': """
        Render a custom download button in the portal for end users to download the related timesheets as Excel file.
    """,
    "author": "Code Agency",
    "website": "https://codeagency.be",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['account', 'sale', 'hr_timesheet'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}
