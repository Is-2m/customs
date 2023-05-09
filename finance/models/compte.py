from odoo import models, fields


class Compte(models.Model):
    _name = "finance.compte"
    _rec_name = "num_compte"

    order_recette_ids = fields.One2many('finance.ordre.recette', 'compte_id', string='Ordres Recette', required=True, )
    num_compte = fields.Char(string='Numéro de compte', required=True, )
    name = fields.Char(string='Nom du compte')
    type = fields.Selection([('debits', 'Debits'), ('credits', 'Credits'), ], string='Type de compte', required=True, )
