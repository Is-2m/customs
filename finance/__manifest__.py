




{
    'name': "Finance",
    'description': """
        Gestion finance
        ====================
        Gestion des payments, des engaments, des situations budgetaires 
    """,
    'depends': ['base', 'web'],
    'assets': {
        'web.report_assets_pdf': [
            '/finance/static/src/css/report.css'
        ]
    },
    'data': [
        'security/ir.model.access.csv',
        'views/template.xml',
        'views/ligne_recette_view.xml',
        'views/ordre_recette_view.xml',
        'views/compte_view.xml',
        'views/debiteur_view.xml',
        # 'views/ordonnateur_view.xml',

        'views/article_views.xml',
        'views/paragraph_views.xml',
        'views/ligne_views.xml',
        'views/engagement_views.xml',
        'views/menu.xml',
        'reports/report_action.xml',
        'reports/order_recette_report.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False
}
