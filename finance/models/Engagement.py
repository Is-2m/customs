from odoo import models, fields, api


class Engagement(models.Model):
    _name = 'finance.engagement'

    # ---------------------------------------------Relations----------------------------------------------
    ligne_id = fields.Many2one("finance.ligne", string='Ligne', ondelete="set null")
    produit_ids = fields.Many2many("finance.produit", string="Produits")
    engagement_produit_ids = fields.One2many('finance.engagement_produit', 'engagement_id', string="Engagement*")

    service_ids = fields.Many2many("finance.service", string="Services")
    # ----------------------------------------------------------------------------------------------------

    # montant = fields.Float(string='Montant')
    date_engagement = fields.Date(string='Date Engagement', default=lambda self: (fields.Date.today()))
    # -------------------------------------Computed------------------------------------------------
    # total_price = fields.Float(compute="", store=False)
    montant = fields.Float(string='Montant', compute='_get_total_price', readonly=True, store=True)

    # product_total_price = fields.Float(compute="_get_product_price", store=False)

    # ---------------------------------------------------------------------------------------------
    @api.depends('engagement_produit_ids.product_total_price')
    def _get_total_price(self):
        total = sum(self.mapped('engagement_produit_ids.product_total_price'))
        self.montant = total

    # for eng in self:
    #     for prod in eng.engagement_produit_ids:
    #         eng.total_price += prod.product_total_price
