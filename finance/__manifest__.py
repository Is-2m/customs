{
    'name': "Finance",
    'description': """
        Administration Finance
        ====================
        Gestion des payments, des engagements, des situations budgetaires 
    """,
    'depends': ['base', 'web'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web.report_assets_pdf': [
            '/finance/static/src/css/report.css',
            '/finance/static/src/css/bon_com_report.css'
        ]
    },
    'data': [
        'security/ir.model.access.csv',
        'views/ligne_recette_view.xml',
        'views/ordre_recette_view.xml',
        'views/compte_view.xml',
        'views/debiteur_view.xml',
        'views/article_views.xml',
        'views/paragraph_views.xml',
        'views/ligne_views.xml',
        'views/bon_commande_view.xml',
        'views/piece_jointe_view.xml',
        'views/fournisseur_view.xml',
        'views/engagement_produit_view.xml',
        'views/produit_view.xml',
        'views/ordre_payment_view.xml',
        'views/detail_morasse_view.xml',
        'views/morasse_view.xml',
        'views/menu.xml',
        'reports/report_action.xml',
        'reports/order_recette_report.xml',
        'reports/bon_commande_report.xml',
        'reports/ordre_paiement_report.xml'
    ]
}
