from odoo import fields, models, api


class EngagementService(models.Model):
    _name = 'finance.engagement_service'

    # _description = 'Description'

    # id = fields.Id('ID')
    # # -------------------------------------Relations------------------------------------------------
    # engagement_id = fields.Many2one('finance.engagement', string='Engagement')
    # service_id = fields.Many2one('finance.service', string='Service')
    #
    # # -------------------------------------Computed------------------------------------------------
    # service_price = fields.Float(compute="_get_service_price", store=False)
    #
    # # ---------------------------------------------------------------------------------------------
    # @api.depends('service_id.prix')
    # def _get_product_price(self):
    #     for o in self:
    #         o.service_price = o.service_id.prix if o.service_id else 0.0