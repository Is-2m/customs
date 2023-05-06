import datetime

from odoo import fields, models, api


class ordre_recette(models.Model):
    _name = "or.ordre.recette"

    ordonnateur_id = fields.Many2one('or.ordonnateur')
    debiteur_id = fields.Many2one('or.debiteur')
    nature = fields.Many2one('or.ligne.recette', 'code')
    facturation = fields.Char()
    marche = fields.Char()
    contrat = fields.Char()
    decision = fields.Char()
    ac_banque = fields.Char()
    convention = fields.Char()
    explication = fields.Text()
    montant_chiffre = fields.Float()
    montant_lettre = fields.Char()
    type = fields.Selection([("subvention d'exploitation", "Subvention d'exploitation"),
                             ("subvention d'investissement", "Subvention d'investissement")], string='Type')
    piece_jointe_ids = fields.One2many('or.piece_jointe', 'recette_id', string="piece jointes")

    # action in model :
    # def my_action(self):
    #     # Implement the action here
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'home.xml',
    #         'res_model': 'or.ordre.recette',
    #         'view_mode': 'form',
    #     }

    # name = fields.Char('Plan Name', required=True)
    # sequence = fields.Integer('Sequence', default=10)

    # how to create constraints on some columns of the table
    _sql_constraints = [
        ('check_montant', 'CHECK( montant_chiffre >= 0)', 'Le montant ne peut pas etre negatif.'),
    ]
