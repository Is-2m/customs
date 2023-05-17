from odoo import models, fields


class Engagement(models.Model):
    _name = 'finance.engagement'

    # ---------------------------------------------Relations----------------------------------------------
    ligne_id = fields.Many2one("finance.ligne", string='Ligne', ondelete="set null")
    produit_ids = fields.Many2many("finance.produit", 'finance_engagement_produit',
                                   'engagement_id', 'produit_id', string="Engagements")
    service_ids = fields.Many2many("finance.fournisseur", string="Services")
    # ----------------------------------------------------------------------------------------------------

    montant = fields.Float(string='Montant')
    date_engagement = fields.Date(string='Date Engagement')
