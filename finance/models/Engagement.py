from odoo import models, fields


class Engagement(models.Model):
    _name = 'finance.engagement'

    # ---------------------------------------------Relations----------------------------------------------
    ligne_id = fields.Many2one("finance.ligne", string='Ligne', ondelete="set null")
    produit_ids = fields.Many2many(comodel_name="finance.produit", relation='finance_engagement_produit',
                                   column1='engagement_id', column2='produit_id', string="Engagements")
    service_ids = fields.Many2many("finance.fournisseur", string="Services")
    # ----------------------------------------------------------------------------------------------------

    montant = fields.Float(string='Montant')
    date_engagement = fields.Date(string='Date Engagement')
