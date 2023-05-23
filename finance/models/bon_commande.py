from odoo import fields, models, api


class BonCommande(models.Model):
    _name = 'finance.bon.commande'
    _description = 'Description'
    _inherit = "finance.payment"

    # order_payment_ids = fields.One2many('finance.ordre_payment', 'payment_id')


    # ---------------------------------------------Computed---------------------------------------
    # ligne = fields.Integer(string='Ligne', compute='_get_ligne_1', readonly=True)
    #
    # @api.depends('engagement_id.ligne_id')
    # def _get_ligne_1(self):
    #     for eng in self:
    #         eng.ligne = eng.engagement_id.ligne_id.code
