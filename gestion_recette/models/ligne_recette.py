from odoo import fields, models


class ligne_recette(models.Model):
    _name = "or.ligne.recette"

    code = fields.Integer("Nature de la recette", primary_key=True)
    label = fields.Char("Intitule de la recette")
    or_ids = fields.One2many('or.ordre.recette','nature',string="Ordres de recette")