from odoo import fields, models


class ligne_recette(models.Model):
    _name = "or.ligne.recette"
    _description = "Ligne Recette Enregistrements"

    id = fields.Integer("Id de la ligne", primary_key=True)
    code = fields.Integer("Nature de la recette", required=True, index=True)
    label = fields.Char("Intitule de la recette")
    or_ids = fields.One2many('or.ordre.recette', 'nature', string="Ordres de recette")

    _sql_constraints = [
        ('field_unique',
         'unique(code)',
         'Choisir une autre valeur - il faut donner un valeur unique')
    ]
