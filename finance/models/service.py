from odoo import fields, models, api


class Service(models.Model):
    _name = 'finance.service'
    # --------------------------------Relations----------------------------------------------------
    engagement_ids = fields.Many2many('finance.engagement', string="Engagements")
    fournisseur_id = fields.Many2one("finance.fournisseur", "Fournisseur")

    name = fields.Char("Intitule")
    prix = fields.Float("Prix")
    description = fields.Char("Description")
