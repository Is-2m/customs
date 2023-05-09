{
    'name':'Gestion Financiere',
    'depends':['base'],
    'application': True,
    'data':[
        'security/ir.model.access.csv',

        'views/article_views.xml',
        'views/paragraph_views.xml',
        'views/ligne_views.xml',
        'views/engagement_views.xml',
        'views/gestion_financiere_menus.xml'

    ]
}