from odoo import models, fields


class Compte(models.Model):
    _name = "finance.compte"
    _rec_name = "num_compte"

    # -----------------------------------Relations-----------------------------------------------
    order_recette_ids = fields.One2many('finance.ordre.recette', 'compte_id', string='Ordres Recette', required=False, )
    fournisseur_id = fields.Many2one("finance.fournisseur", string="Fournisseur")
    payment_ids = fields.One2many("finance.payment", 'compte_id', string="Payments")
    # --------------------------------------------------------------------------------------------
    num_compte = fields.Char(string='Numéro de compte', required=True, )
    type = fields.Selection([('debits', 'Debits'), ('credits', 'Credits'), ], string='Type de compte', required=True, )
    name = fields.Char(string='Nom du Compte')
    bank_name = fields.Char(string="Nom de Banque")
