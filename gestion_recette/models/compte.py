from odoo import models, fields


class Compte(models.Model):
    _name = "or.compte"

    ordonnateur_id = fields.Many2one('or.ordonnateur', string='Ordonnateur', required=True, )
    num_compte = fields.Char(
        string='Numéro de compte',
        required=True,
    )
    name = fields.Char(
        string='Nom du compte'
    )
    type = fields.Selection([
        ('debits', 'Debits'),
        ('credits', 'Credits'),
    ],
        string='Type de compte',
        required=True,
    )
