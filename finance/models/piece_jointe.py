from odoo import models, fields


class PieceJoint(models.Model):
    _name = 'finance.piece_jointe'

    name = fields.Char()
    file_data = fields.Binary("Ficher")
    order_recette_ids = fields.Many2many('finance.ordre.recette', string='Ordres Recette')

    # Any other fields for Ordonnateur table
