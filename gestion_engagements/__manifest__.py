{
    'name':'Gestion Engagements',
    'depends':['base', 'gestion_financiere'],
    'application': True,
    'data':[
        'security/ir.model.access.csv',

        'views/engagement_views.xml',
        'views/gestion_engagements_menus.xml',

    ]
}