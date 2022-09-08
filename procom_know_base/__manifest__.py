# -*- coding: utf-8 -*-
{
    'name': "Procom Knowledge Base",

    'summary': """
        Knowledge Base Module with Helpdesk/Field Service Integration""",

    'description': """
        Features:\n
        - KB Categories\n
        - KB Tags\n
        - KB Question/Answers\n
        - KB Integration with Helpdesk / Field Service\n
    """,

    "author": "Code Agency",
    "website": "https://codeagency.be",

    'version': '0.1',

    'depends': ['helpdesk', 'helpdesk_timesheet', 'project'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/inherited_helpdesk_task_view.xml',
    ],
}
