from odoo import models, fields, api


class Engagement(models.Model):
    _name = 'finance.engagement'
    _rec_name = 'code_year'

    # ---------------------------------------------Relations----------------------------------------------
    ligne_id = fields.Many2one("finance.ligne", string='Ligne', ondelete="restrict", required=True, )
    produit_ids = fields.Many2many("finance.produit", string="Produits")
    engagement_produit_ids = fields.One2many('finance.engagement_produit', 'engagement_id', string="Produits*")
    payment_ids = fields.One2many('finance.payment', 'engagement_id', string="Paiement*")

    service_ids = fields.Many2many("finance.service", string="Services")
    # ----------------------------------------------------------------------------------------------------

    code = fields.Integer(string='Code')
    date_engagement = fields.Date(string='Date Engagement', default=lambda self: (fields.Date.today()))
    # -------------------------------------Computed------------------------------------------------
    montant = fields.Float(string='Montant', compute='_get_total_price', readonly=True, store=True)
    code_year = fields.Char(string='Engagement Code', compute='_get_engagement_code_by_year', readonly=True)

    # total_price = fields.Float(compute="", store=False)
    # product_total_price = fields.Float(compute="_get_product_price", store=False)

    # ---------------------------------------------------------------------------------------------
    @api.depends('engagement_produit_ids.product_total_price')
    def _get_total_price(self):
        total = sum(self.mapped('engagement_produit_ids.product_total_price'))
        self.montant = total

    @api.depends('code', 'date_engagement')
    def _get_engagement_code_by_year(self):
        for eng in self:
            code_by_year = f"{eng.code}/{eng.date_engagement.year}"
            eng.code_year = code_by_year

    # for eng in self:
    #     for prod in eng.engagement_produit_ids:
    #         eng.total_price += prod.product_total_price
