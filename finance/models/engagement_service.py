from odoo import fields, models, api


class EngagementService(models.Model):
    _name = 'finance.engagement_service'
    # _description = 'Description'

    name = fields.Char()
