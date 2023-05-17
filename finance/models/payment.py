from odoo import fields, models, api


class Payment(models.Model):
    _name = 'finance.payment'
    _description = 'Mother Table for all payment types'

    # ----------------------------------------------Relations-----------------------------------------
    compte_id = fields.Many2one('finance.compte', string='Compte')

    # ------------------------------------------------------------------------------------------------
    name = fields.Char()
    montant = fields.Float(string="Montant")
    date = fields.Date(string="Date", default=lambda self: (fields.Datetime.today()))
