from odoo import fields, models, api


class EngagementProduit(models.Model):
    _name = 'finance.engagement_produit'
    # _description = 'Description'

    # name = fields.Char()
    engagement_id = fields.Many2one('finance.engagement', string='Engagement')
    product_id = fields.Many2one('finance.produit', string='Product')
    quantity = fields.Integer(string='Quantite Acheter')
