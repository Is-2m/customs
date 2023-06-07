from odoo import fields, models, api


class Produit(models.Model):
    _name = 'finance.produit'
    _rec_name = 'display_name'
    # --------------------------------Relations----------------------------------------------------
    engagement_produit_ids = fields.One2many('finance.engagement_produit', 'produit_id', string='Product*')
    fournisseur_id = fields.Many2one("finance.fournisseur", "Fournisseur")
    # ------------------------------------------------------------------------------------

    name = fields.Char("Designation", required=True)
    prix = fields.Float("Prix Unitaire")
    description = fields.Char("Description")
    type = fields.Selection(string="Type", selection=[
        ('produit', 'Produit'),
        ('service', 'Service'),
        ('travaux', 'Travaux')
    ], default='produit')
    display_name = fields.Char(compute='_get_display_name')

    @api.depends('name', 'fournisseur_id.name')
    def _get_display_name(self):
        for prod in self:
            prod.display_name = f"{prod.name} " \
                                f"{prod.description if prod.description else ''} " \
                                f"{' - ' + prod.fournisseur_id.name if prod.fournisseur_id else ''}"
