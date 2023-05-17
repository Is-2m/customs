from odoo import fields, models, api


class Produit(models.Model):
    _name = 'finance.produit'
    # --------------------------------Relations----------------------------------------------------
    engagement_ids = fields.Many2many(comodel_name='finance.engagement', relation='finance_engagement_produit',
                                      column1='produit_id',
                                      column2='engagement_id', string="Engagements")
    fournisseur_id = fields.Many2one("finance.fournisseur", "Fournisseur")
    # ------------------------------------------------------------------------------------

    name = fields.Char("Designation")
    prix = fields.Monetary("Prix Unitaire")
    description = fields.Char("Description")
