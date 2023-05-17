from odoo import fields, models, api


class Produit(models.Model):
    _name = 'finance.produit'
    # --------------------------------Relations----------------------------------------------------
    engagement_ids = fields.Many2many('finance.engagement', 'finance_engagement_produit',
                                      'produit_id', 'engagement_id', string="Engagements")
    fournisseur_id = fields.Many2one("finance.fournisseur", "Fournisseur")
    # ------------------------------------------------------------------------------------

    name = fields.Char("Designation")
    prix = fields.Float("Prix Unitaire")
    description = fields.Char("Description")
