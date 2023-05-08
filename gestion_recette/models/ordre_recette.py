from odoo import fields, models, api
from num2words import num2words


class ordre_recette(models.Model):
    _name = "or.ordre.recette"
    _description = "Ordre Recette Enregistrement"

    ordonnateur_id = fields.Many2one('or.ordonnateur', string="Ordonnateur ID", required=True)
    nature_id = fields.Many2one('or.ligne.recette', 'Nature Recette', required=True)
    debiteur_id = fields.Many2one('or.debiteur', string="Debiteur ID", required=True)
    facturation = fields.Char(string="Facturation n")
    description = fields.Char(string="Description")
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
    # piece_jointe_ids = fields.Char(string="")
    total_montant_chiffre = fields.Float(compute='_compute_total_montant_chiffre', string="Total", store=True)
    num_compte = fields.Char(string='Numero Compte', compute='_get_num_compte', store=False)
    type_compte = fields.Char(string='Type Compte', compute='_get_type_compte', store=False)


    @api.depends('montant_chiffre')
    def _compute_total_montant_chiffre(self):
        total = sum(self.mapped('montant_chiffre'))
        self.total_montant_chiffre = total

    @api.depends('montant_chiffre')
    def _compute_montant_lettre(self):
        for rec in self:
            montant_chiffre = rec.montant_chiffre
            if montant_chiffre == 0:
                rec.montant_lettre = "zéro DH".upper()
            else:
                # Convert the float to an integer to get rid of the decimal point
                integer_part = int(montant_chiffre)
                # Convert the integer part to words
                words = num2words(integer_part, lang='fr')
                # Add the word for the currency (euros) and the decimal part, if there is one
                decimal_part = int(round((montant_chiffre - integer_part) * 100))
                if decimal_part == 0:
                    rec.montant_lettre = f"{words} DH".upper()
                else:
                    rec.montant_lettre = f"{words} DH {num2words(decimal_part, lang='fr')} centimes".upper()


    @api.depends('ordonnateur_id.comptes.num_compte')
    def _get_num_compte(self):
        for ordre_recette in self:
            ordre_recette.num_compte = ordre_recette.ordonnateur_id.comptes.num_compte if ordre_recette.ordonnateur_id or ordre_recette.ordonnateur_id.comptes else ''

    @api.depends('ordonnateur_id.comptes.type')
    def _get_type_compte(self):
        for ordre_recette in self:
            ordre_recette.type_compte = ordre_recette.ordonnateur_id.comptes.type if ordre_recette.ordonnateur_id or ordre_recette.ordonnateur_id.comptes else ''


_sql_constraints = [
        ('check_montant', 'CHECK( montant_chiffre >= 0)', 'Le montant ne peut pas etre negatif.'),
    ]
