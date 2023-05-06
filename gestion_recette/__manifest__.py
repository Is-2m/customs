{
    'name': "Gestion Recette",
    'description': """
        Gestion finance
        ====================
        Gestion des payments, des engaments, des situations budgetaires 
    """,
    'depends': ['base', 'web'],

    'data': [
        'security/ir.model.access.csv',
        'views/template.xml',
        'views/menu.xml',
        'views/ligne_recette_view.xml',
        'views/ordre_recette_view.xml',
        'reports/test_report_action.xml',
        'reports/or_template.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False
}
