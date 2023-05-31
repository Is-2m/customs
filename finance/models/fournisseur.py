from odoo import fields, models, api


class Fournisseur(models.Model):
    _name = 'finance.fournisseur'
    # ----------------------------Relations--------------------------------
    compte_ids = fields.One2many("finance.compte", "fournisseur_id", "Comptes")
    product_ids = fields.One2many("finance.produit", "fournisseur_id", "Produits")
    # ----------------------------------------------------------------------
    name = fields.Char("Nom ou Raison Sociale")
    adresse = fields.Char("Adresse")
