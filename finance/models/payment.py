from odoo import fields, models, api


class Payment(models.Model):
    _name = 'finance.payment'
    _description = 'Mother Table for all payment types'

    # ----------------------------------------------Relations-----------------------------------------
    compte_id = fields.One2many('finance.compte', string='Compte')

    # ------------------------------------------------------------------------------------------------
    name = fields.Char()
    montant = fields.Monetary(string="Montant")
    date = fields.Monetary(string="Date", default=lambda self: (fields.Datetime.today()))
