from odoo import fields, models, api


class Produit(models.Model):
    _name = 'finance.produit'
    # --------------------------------Relations----------------------------------------------------
    engagement_produit_ids = fields.One2many('finance.engagement_produit', 'produit_id', string='Product*')
    fournisseur_id = fields.Many2one("finance.fournisseur", "Fournisseur")
    # ------------------------------------------------------------------------------------

    name = fields.Char("Designation")
    prix = fields.Float("Prix Unitaire")
    description = fields.Char("Description")
    type = fields.Selection(string="Type", selection=[
        ('produit', 'Produit'),
        ('service', 'Service'),
        ('travaux', 'Travaux')
    ])
