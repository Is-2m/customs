from odoo import fields, models, api
from num2words import num2words


class OrdreRecette(models.Model):
    _name = "finance.ordre.recette"
    _description = "Ordre Recette Enregistrement"
    _sql_constraints = [
        ('check_year', 'CHECK (year >= 1900 AND year <= 2300)',
         'l\'année doit se situer entre 1900 et 2300 !!'),
        ('check_montant', 'CHECK( montant_chiffre >= 0)', 'Le montant ne peut pas être négatif.'),
    ]

    # ------------------------------------ Relations --------------------------------
    nature_id = fields.Many2one('finance.ligne.recette', 'Nature Recette', required=True)
    debiteur_id = fields.Many2one('finance.debiteur', string="Debiteur ID", required=True)
    compte_id = fields.Many2one('finance.compte', string='Compte', required=True)
    piece_jointe_ids = fields.Many2many('finance.piece_jointe', string="Pieces Jointes")

    # ------------------------------------- Fields ----------------------------------

    facturation = fields.Char(string="Facturation N°")
    description = fields.Char(string="Explication")
    marche = fields.Char(string="Marche N°")
    contrat = fields.Char(string="Contract N°")
    decision = fields.Char(string="Decision N°")
    ac_banque = fields.Char(string="A.C Bangue N°")
    convention = fields.Char(string="Convention N°")
    year = fields.Integer(string="Annee", default=lambda self: fields.Datetime.today().year, required=True)
    montant_chiffre = fields.Float(string="Montant Chiffre", required=True)
    type = fields.Selection([("subvention d'exploitation", "Subvention d'exploitation"),
                             ("subvention d'investissement", "Subvention d'investissement")], string='Type',
                            required=True)
    # ---------------------------------------Computed Fields----------------------------------
    total_montant_chiffre = fields.Float(compute='_compute_total_montant_chiffre', string="Total", store=True)
    montant_lettre = fields.Char(compute="_compute_montant_lettre", string="Montant Lettre", store=True)

    formated_year = fields.Char(compute='_year_withou_comma', string="Annee", store=False)


    # ------------------------------Api.Dependes-------------------------------------
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
                integer_part = int(montant_chiffre)
                words = num2words(integer_part, lang='fr')
                decimal_part = int(round((montant_chiffre - integer_part) * 100))
                if decimal_part == 0:
                    rec.montant_lettre = f"{words} DH".upper()
                else:
                    rec.montant_lettre = f"{words} DH {num2words(decimal_part, lang='fr')} centimes".upper()

    @api.depends('year')
    def _year_withou_comma(self):
        for record in self:
            record.formated_year = '{:04d}'.format(record.year)
