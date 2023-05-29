from odoo import fields, models, api


class BonCommande(models.Model):
    _name = 'finance.bon.commande'
    _description = 'Description'
    _inherit = "finance.engagement"
    # _sql_constraints = [
    #     ("finance.bon_com_PKey", "primary key(engagement_id)", '')
    # ]

    order_payment_ids = fields.One2many('finance.ordre_payment', 'bon_com_id')
    # engagement_id = fields.Many2one('finance.engagement')

    # ---------------------------------------------Computed---------------------------------------
    # ligne = fields.Integer(string='Ligne', compute='_get_ligne_1', readonly=True)
    #
    # @api.depends('engagement_id.ligne_id')
    # def _get_ligne_1(self):
    #     for eng in self:
    #         eng.ligne = eng.engagement_id.ligne_id.code
