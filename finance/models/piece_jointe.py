from odoo import models, fields


class PieceJoint(models.Model):
    _name = 'finance.piece_jointe'

    name = fields.Char()
    file_data = fields.Binary()
    file_name = fields.Char()

    # --------------------------------Relations--------------------------------------------------
    order_recette_ids = fields.Many2many('finance.ordre.recette', string='Ordres Recette')
    order_payment_ids = fields.Many2many('finance.ordre_payment', string='Ordres Paiements')
    # -------------------------------------------------------------------------------------------

    # Any other fields for Ordonnateur table
