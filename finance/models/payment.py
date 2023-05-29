from odoo import fields, models, api
from num2words import num2words


class Payment(models.AbstractModel):
    _name = 'finance.payment'
    _description = 'Mother Table for all payment types'
    _rec_name = 'code_year'

    id = fields.Id(string="ID")
    # ----------------------------------------------Relations-----------------------------------------
    compte_id = fields.Many2one('finance.compte', string='Compte')
    # engagement_id = fields.Many2one('finance.engagement', string='Engagement')
    # order_payment_ids = fields.One2many('finance.ordre_payment', 'payment_id')
    # ------------------------------------------------------------------------------------------------
    code = fields.Integer()
    date = fields.Date(string="Date", default=lambda self: (fields.Datetime.today()))
    description = fields.Char(string="Destination et utilisation")

    # --------------------------------Computed---------------------------------
    montant = fields.Float(string="Montant", compute='_get_total_ht', readonly=True, store=True)
    code_year = fields.Char(string='Code', compute='_get_code_by_year', readonly=True)
    ligne = fields.Integer(string='Ligne', compute='_get_ligne', readonly=True)
    ligne_label = fields.Char(string='Ligne Rubrique', compute='_get_ligne_rubrique', readonly=True)
    paragraphe = fields.Integer(string='Paragraphe', compute='_get_paragraphe', readonly=True)
    article = fields.Integer(string='Article', compute='_get_article', readonly=True)
    tva_montant = fields.Float(string='TVA', compute='_get_tva', readonly=True)
    total_ttc = fields.Float(string="Total TTC", compute='_get_total_ttc')
    total_ttc_letter = fields.Char(string="Total TTC", compute='_get_total_ttc_lettre')
    fournisseur = fields.Char(string="Fournisseur", compute='_get_fournisseur_produit')
    fournisseur_adresse = fields.Char(string="Fournisseur", compute='_get_adresse_fournisseur_produit')
    full_ligne_code = fields.Char(string="Ligne", compute='_get_art_para_ligne')
    display_name = fields.Char("Display_name")

    @api.depends('total_ttc')
    def _get_total_ttc_lettre(self):
        for rec in self:
            montant_chiffre = rec.total_ttc
            if montant_chiffre == 0:
                rec.total_ttc_letter = "zéro DH".upper()
            else:
                integer_part = int(montant_chiffre)
                words = num2words(integer_part, lang='fr')
                decimal_part = int(round((montant_chiffre - integer_part) * 100))
                if decimal_part == 0:
                    rec.total_ttc_letter = f"{words} DH".upper()
                else:
                    rec.total_ttc_letter = f"{words} DH {num2words(decimal_part, lang='fr')} centimes".upper()

    @api.depends('code', 'date')
    def _get_code_by_year(self):
        for pay in self:
            code_by_year = f"{pay.code}/{pay.date.year}"
            pay.code_year = code_by_year

    @api.depends('engagement_id.montant')
    def _get_total_ht(self):
        for pay in self:
            pay.montant = pay.engagement_id.montant

    @api.depends('engagement_id.detail_morasse_id.ligne_id')
    def _get_art_para_ligne(self):
        for eng in self:
            line = eng.engagement_id.detail_morasse_id.ligne_id
            full_code = f"{line.article_code}/{line.paragraph_code}/{line.code}"
            eng.full_ligne_code = full_code

    @api.depends('engagement_id.detail_morasse_id.ligne_id')
    def _get_ligne(self):
        for eng in self:
            eng.ligne = eng.engagement_id.detail_morasse_id.ligne_id.code

    @api.depends('engagement_id.detail_morasse_id.ligne_id')
    def _get_ligne_rubrique(self):
        for eng in self:
            eng.ligne_label = eng.engagement_id.detail_morasse_id.ligne_id.label

    @api.depends('engagement_id.detail_morasse_id.ligne_id')
    def _get_paragraphe(self):
        for eng in self:
            eng.paragraphe = eng.engagement_id.detail_morasse_id.ligne_id.paragraph_code

    @api.depends('engagement_id.detail_morasse_id.ligne_id')
    def _get_article(self):
        for eng in self:
            eng.article = eng.engagement_id.detail_morasse_id.ligne_id.article_code

    @api.depends('montant')
    def _get_tva(self):
        for eng in self:
            eng.tva_montant = eng.montant * 0.2

    @api.depends('montant')
    def _get_total_ttc(self):
        for eng in self:
            eng.total_ttc = eng.montant * 1.2

    # @api.depends('engagement_id.service_ids.fournisseur_id')
    # def _get_fournisseur_service(self):
    #     for eng in self:
    #         eng.total_ttc = eng.montant * 1.2

    @api.depends('engagement_id.engagement_produit_ids.product_fournisseur')
    def _get_fournisseur_produit(self):
        for eng in self:
            for p in eng.engagement_id.engagement_produit_ids:
                eng.fournisseur = p.product_fournisseur

    @api.depends('engagement_id.engagement_produit_ids.product_fournisseur')
    def _get_adresse_fournisseur_produit(self):
        for eng in self:
            for p in eng.engagement_id.engagement_produit_ids:
                eng.fournisseur_adresse = p.produit_id.fournisseur_id.adresse
