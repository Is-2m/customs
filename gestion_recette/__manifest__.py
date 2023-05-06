{
    'name': "Gestion Recette",
    'description': """
        Gestion finance
        ====================
        Gestion des payments, des engaments, des situations budgetaires 
    """,
    'depends': ['base','web'],

    'data':[
        'views/home.xml',
        'security/ir.model.access.csv',
        'reports/test_report_action.xml',
        'reports/or_template.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False
}
