from odoo import models, fields

class PieceJointe(models.Model):
    _name = 'or.piece_jointe'

    recette_id = fields.Many2one('or.ordre.recette')
    filename = fields.Char()
    file_data = fields.Binary()
