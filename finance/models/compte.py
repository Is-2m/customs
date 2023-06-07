from odoo import models, fields, api


class Compte(models.Model):
    _name = "finance.compte"
    _rec_name = "display_name"

    num_compte = fields.Char(string='Numéro de compte', required=True, )
    type = fields.Selection([('debits', 'Debits'), ('credits', 'Credits'), ], string='Type de compte', required=True, )
    name = fields.Char(string='Nom du Compte', default='')
    bank_name = fields.Char(string="Nom de Banque")
    # -----------------------------------Relations-----------------------------------------------
    order_recette_ids = fields.One2many('finance.ordre.recette', 'compte_id', string='Ordres Recette', required=False, )
    fournisseur_id = fields.Many2one("finance.fournisseur", string="Fournisseur")
    # --------------------------------------------------------------------------------------------
    display_name = fields.Char(string="Compte", compute='_get_account_name', readonly=True)

    @api.depends('num_compte')
    def _get_account_name(self):
        for acc in self:
            if acc.fournisseur_id:
                acc.display_name = f"{acc.fournisseur_id.name} {acc.name if acc.name else ''} {str(acc.num_compte)[:5]} - {acc.bank_name}"
            else:
                acc.display_name = f"{acc.name if acc.name else ''} {str(acc.num_compte)[:5]} - {acc.bank_name}"
