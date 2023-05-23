from num2words import num2words
from odoo import fields, models, api


class OrderPayment(models.Model):
    _name = 'finance.ordre_payment'
    _description = 'Description'
    _rec_name = 'code_year'

    facture = fields.Char(string="Facture N°")
    code = fields.Integer(string="Code")
    montant = fields.Float(string="Montant")
    date = fields.Date(string="Date", default=lambda self: (fields.Date.today()))
    # -------------------------------- Relations ----------------------------------------------
    piece_jointe_ids = fields.Many2many('finance.piece_jointe', string="Pieces Jointes")
    payment_id = fields.Many2one("finance.payment")
    # --------------------------------- Computed ----------------------------------------------
    montant_letter = fields.Char(string="Montant Letter", compute='_get_montant_lettre')
    code_year = fields.Char(string='Code', compute='_get_code_by_year', readonly=True)
    ligne = fields.Integer(string='Ligne', compute='_get_ligne', readonly=True)
    ligne_label = fields.Char(string='Ligne Rubrique', compute='_get_ligne_rubrique', readonly=True)
    paragraphe = fields.Integer(string='Paragraphe', compute='_get_paragraphe', readonly=True)
    article = fields.Integer(string='Article', compute='_get_article', readonly=True)
    num_compte = fields.Char(string="Numéro Compte", compute="_get_num_compte")
    bank_name = fields.Char(string="Numéro Compte", compute="_get_bank_name")
    fournisseur = fields.Char(string="Fournisseur", compute='_get_fournisseur_produit')
    fournisseur_adresse = fields.Char(string="Fournisseur", compute='_get_adresse_fournisseur_produit')
    full_ligne_code = fields.Char(string="Ligne", compute='_get_art_para_ligne')

    @api.depends('montant')
    def _get_montant_lettre(self):
        for rec in self:
            montant_chiffre = rec.montant
            if montant_chiffre == 0:
                rec.montant_letter = "zéro DH".upper()
            else:
                integer_part = int(montant_chiffre)
                words = num2words(integer_part, lang='fr')
                decimal_part = int(round((montant_chiffre - integer_part) * 100))
                if decimal_part == 0:
                    rec.montant_letter = f"{words} DH".upper()
                else:
                    rec.montant_letter = f"{words} DH {num2words(decimal_part, lang='fr')} centimes".upper()

    @api.depends('code', 'date')
    def _get_code_by_year(self):
        for pay in self:
            code_by_year = f"{pay.code}/{pay.date.year}"
            pay.code_year = code_by_year

    @api.depends('payment_id.ligne')
    def _get_ligne(self):
        for pay in self:
            pay.ligne = pay.payment_id.ligne

    @api.depends('payment_id.ligne')
    def _get_art_para_ligne(self):
        for pay in self:
            pay.full_ligne_code = pay.payment_id.full_ligne_code

    @api.depends('payment_id.compte_id.num_compte')
    def _get_num_compte(self):
        for pay in self:
            pay.num_compte = pay.payment_id.compte_id.num_compte

    @api.depends('payment_id.compte_id.bank_name')
    def _get_bank_name(self):
        for pay in self:
            pay.bank_name = pay.payment_id.compte_id.bank_name

    @api.depends('payment_id.ligne_label')
    def _get_ligne_rubrique(self):
        for pay in self:
            pay.ligne_label = pay.payment_id.ligne_label

    @api.depends('payment_id.paragraphe')
    def _get_paragraphe(self):
        for pay in self:
            pay.paragraphe = pay.payment_id.paragraphe

    @api.depends('payment_id.article')
    def _get_article(self):
        for pay in self:
            pay.article = pay.payment_id.article

    @api.depends('payment_id.engagement_id.engagement_produit_ids.product_fournisseur')
    def _get_fournisseur_produit(self):
        for pay in self:
            if pay.payment_id and pay.payment_id.engagement_id:
                for p in pay.payment_id.engagement_id.engagement_produit_ids:
                    pay.fournisseur = p.product_fournisseur if p.product_fournisseur else ''
            else:
                pay.fournisseur = ""

    @api.depends('payment_id.engagement_id.engagement_produit_ids.product_fournisseur')
    def _get_adresse_fournisseur_produit(self):
        for pay in self:
            if pay.payment_id and pay.payment_id.engagement_id:
                for p in pay.payment_id.engagement_id.engagement_produit_ids:
                    pay.fournisseur_adresse = p.produit_id.fournisseur_id.adresse if p.produit_id.fournisseur_id else ''
            else:
                pay.fournisseur_adresse = ""
