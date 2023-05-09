from odoo import models, fields
class Engagement(models.Model):
    _name = 'finance.engagement'

    montant = fields.Float(string='Montant')
    date_engagement = fields.Date(string='Date Engagement')
    ligne_id = fields.Many2one("finance.ligne", string='Ligne',ondelete="set null")
