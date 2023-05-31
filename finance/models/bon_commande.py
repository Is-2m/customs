from num2words import num2words
from odoo import fields, models, api


class BonCommande(models.Model):
    _name = 'finance.bon.commande'
    _description = 'Description'
    _inherit = "finance.engagement"
    # _sql_constraints = [
    #     ("finance.bon_com_PKey", "primary key(engagement_id)", '')
    # ]

    # ------------------------------------- Relations -------------------------------------------

    order_payment_ids = fields.One2many('finance.ordre_payment', 'bon_com_id')
    engagement_produit_ids = fields.One2many('finance.engagement_produit', 'bon_com_id', string="Produits*")

    # ------------------------------------------ Computed ---------------------------------------

    code_year = fields.Char(string='Engagement Code', compute='_get_engagement_code_by_year', readonly=True)
    ligne = fields.Integer(string='Ligne', compute='_get_ligne', readonly=True)
    ligne_label = fields.Char(string='Ligne Rubrique', compute='_get_ligne_rubrique', readonly=True)
    paragraphe = fields.Integer(string='Paragraphe', compute='_get_paragraphe', readonly=True)
    article = fields.Integer(string='Article', compute='_get_article', readonly=True)
    tva_montant = fields.Float(string='TVA', compute='_get_tva', readonly=True)
    total_ttc = fields.Float(string="Total TTC", compute='_get_total_ttc')
    total_ttc_letter = fields.Char(string="Total TTC", compute='_get_total_ttc_lettre')
    montant = fields.Float(string='Montant', compute='_get_total_price', readonly=True, store=True)
    fournisseur = fields.Char(string="Fournisseur", compute='_get_fournisseur')
    fournisseur_adresse = fields.Char(string="Fournisseur", compute='_get_adresse_fournisseur')
    full_ligne_code = fields.Char(string="Ligne", compute='_get_art_para_ligne')
    display_name = fields.Char(compute='_get_engagement_code_by_year')
    year = fields.Integer(compute='_get_bon_com_year', store=True)

    @api.depends('detail_morasse_id.ligne_id')
    def _get_art_para_ligne(self):
        for eng in self:
            line = eng.detail_morasse_id.ligne_id
            full_code = f"{line.article_code}/{line.paragraph_code}/{line.code}"
            eng.full_ligne_code = full_code

    @api.depends('detail_morasse_id.ligne_id')
    def _get_paragraphe(self):
        for eng in self:
            eng.paragraphe = eng.detail_morasse_id.ligne_id.paragraph_code

    @api.depends('detail_morasse_id.ligne_id')
    def _get_article(self):
        for eng in self:
            eng.article = eng.detail_morasse_id.ligne_id.article_code

    @api.depends('montant')
    def _get_tva(self):
        for eng in self:
            eng.tva_montant = eng.montant * 0.2

    @api.depends('montant')
    def _get_total_ttc(self):
        for eng in self:
            eng.total_ttc = eng.montant * 1.2

    @api.depends('detail_morasse_id.ligne_id')
    def _get_ligne_rubrique(self):
        for eng in self:
            eng.ligne_label = eng.detail_morasse_id.ligne_id.label

    @api.depends('total_ttc')
    def _get_total_ttc_lettre(self):
        for eng in self:
            montant_chiffre = eng.total_ttc
            if montant_chiffre == 0:
                eng.total_ttc_letter = "zéro DH".upper()
            else:
                integer_part = int(montant_chiffre)
                words = num2words(integer_part, lang='fr')
                decimal_part = int(round((montant_chiffre - integer_part) * 100))
                if decimal_part == 0:
                    eng.total_ttc_letter = f"{words} DH".upper()
                else:
                    eng.total_ttc_letter = f"{words} DH {num2words(decimal_part, lang='fr')} centimes".upper()

    @api.depends('detail_morasse_id.ligne_id')
    def _get_ligne(self):
        for eng in self:
            eng.ligne = eng.detail_morasse_id.ligne_id.code

    @api.depends('code', 'date')
    def _get_engagement_code_by_year(self):
        for eng in self:
            code_by_year = f"{eng.code}/{eng.date.year}"
            eng.code_year = code_by_year
            eng.display_name = code_by_year

    @api.depends('engagement_produit_ids.product_total_price')
    def _get_total_price(self):
        total = sum(self.mapped('engagement_produit_ids.product_total_price'))
        self.montant = total

    @api.depends('engagement_produit_ids.product_fournisseur')
    def _get_fournisseur(self):
        for eng in self:
            fournisseur = ''
            for p in eng.engagement_produit_ids:
                if p.produit_id.fournisseur_id:
                    fournisseur = p.product_fournisseur
                    break
            eng.fournisseur = fournisseur

    @api.depends('engagement_produit_ids.product_fournisseur')
    def _get_adresse_fournisseur(self):
        for eng in self:
            adresse_fournisseur = ''
            for p in eng.engagement_produit_ids:
                if p.produit_id.fournisseur_id:
                    adresse_fournisseur = p.produit_id.fournisseur_id.adresse
                    break
            eng.fournisseur_adresse = adresse_fournisseur

    @api.depends('date')
    def _get_bon_com_year(self):
        for bc in self:
            bc.year = bc.date.year
