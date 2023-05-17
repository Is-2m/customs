from odoo import fields, models, api


class Service(models.Model):
    _name = 'finance.service'

    name = fields.Char("Intitule")
    prix = fields.Monetary("Prix")
    description = fields.Char("Description")
    fournisseur_id = fields.Many2one("finance.fournisseur", "Fournisseur")
