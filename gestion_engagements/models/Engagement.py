from odoo import models, fields
from odoo.addons.gestion_financiere.models import Ligne
class Engagement(models.Model):
    _name = 'gestion_engagements.engagement'

    montant = fields.Float(string='Montant')
    date_engagement = fields.Date(string='Date Engagement')
    ligne_id = fields.Many2one("gestion_financiere.ligne", string='Ligne',ondelete="set null")
