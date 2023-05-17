from odoo import fields, models, api


class BonCommande(models.Model):
    _name = 'finance.bon.commande'
    _description = 'Description'
    _inherit = "finance.payment"

    
