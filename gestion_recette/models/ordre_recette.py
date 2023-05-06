from odoo import fields, models, api
from num2words import num2words


class ordre_recette(models.Model):
    _name = "or.ordre.recette"
    _description = "Ordre Recette Enregistrement"

    ordonnateur_id = fields.Many2one('or.ordonnateur', string="Ordonnateur ID", required=True)
    debiteur_id = fields.Many2one('or.debiteur', string="Debiteur ID", required=True)
    nature = fields.Many2one('or.ligne.recette', 'id', required=True)
    facturation = fields.Char(string="Facturation n")
    marche = fields.Char(string="Marche n")
    contrat = fields.Char(string="Contract n")
    decision = fields.Char(string="Decision n")
    ac_banque = fields.Char(string="A.C Bangue n")
    convention = fields.Char(string="Convention n")
    explication = fields.Text(string="Explication")
    montant_chiffre = fields.Float(string="Montant Chiffre", required=True)
    montant_lettre = fields.Char(compute="_compute_montant_lettre", string="Montant Lettre")
    type = fields.Selection([("subvention d'exploitation", "Subvention d'exploitation"),
                             ("subvention d'investissement", "Subvention d'investissement")], string='Type',
                            required=True)
    piece_jointe_ids = fields.One2many('or.piece_jointe', 'recette_id', string="piece jointes")
    total_montant_chiffre = fields.Float(compute='_compute_total_montant_chiffre', string="Total", store=True)

    @api.depends('montant_chiffre')
    def _compute_total_montant_chiffre(self):
        total = sum(self.mapped('montant_chiffre'))
        self.total_montant_chiffre = total

    @api.depends('montant_chiffre')
    def _compute_montant_lettre(self):
        for rec in self:
            montant_chiffre = rec.montant_chiffre
            if montant_chiffre == 0:
                rec.montant_lettre = "zéro"
            else:
                # Convert the float to an integer to get rid of the decimal point
                integer_part = int(montant_chiffre)
                # Convert the integer part to words
                words = num2words(integer_part, lang='fr')
                # Add the word for the currency (euros) and the decimal part, if there is one
                decimal_part = int(round((montant_chiffre - integer_part) * 100))
                if decimal_part == 0:
                    rec.montant_lettre = f"{words}"
                else:
                    rec.montant_lettre = f"{words} DH {num2words(decimal_part, lang='fr')} centimes"

    # action in model :
    # def my_action(self):
    #     # Implement the action here
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'ligne_recette_view.xml',
    #         'res_model': 'or.ordre.recette',
    #         'view_mode': 'form',
    #     }

    # name = fields.Char('Plan Name', required=True)
    # sequence = fields.Integer('Sequence', default=10)

    # how to create constraints on some columns of the table
    _sql_constraints = [
        ('check_montant', 'CHECK( montant_chiffre >= 0)', 'Le montant ne peut pas etre negatif.'),
    ]
