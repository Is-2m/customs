from odoo import models, fields, api


class Ligne(models.Model):
    _name = 'finance.ligne'
    _description = 'Ligne Description'
    _rec_name = 'display_name'


    id = fields.Integer(primary_key=True)
    code = fields.Char(required=True, index=True)
    label = fields.Char(required=True)
    # --------------------------Relations----------------------------------
    paragraph_id = fields.Many2one('finance.paragraph', string='Paragraph', ondelete='cascade')
    detail_ids = fields.One2many('finance.detail_morasse', 'ligne_id')

    # -------------------------------- Compute ------------------------------
    article_code = fields.Char(string='Article Code', compute='_get_article_code', store=False)
    paragraph_code = fields.Char(string='Paragraph Code', compute='_get_paragraph_code', store=False)
    full_code = fields.Char(string="Ligne", compute="_get_full_code", store=True)
    display_name = fields.Char("Ligne", compute="_get_full_code_label", store=True)

    @api.depends('paragraph_id.article_id.code')
    def _get_article_code(self):
        for ligne in self:
            ligne.article_code = ligne.paragraph_id.article_id.code if ligne.paragraph_id and ligne.paragraph_id.article_id else ''

    @api.depends('paragraph_id.code')
    def _get_paragraph_code(self):
        for ligne in self:
            ligne.paragraph_code = ligne.paragraph_id.code if ligne.paragraph_id else ''

    @api.depends('paragraph_id')
    def _get_full_code(self):
        for l in self:
            l.full_code = f"{l.paragraph_id.article_id.code}/{l.paragraph_id.code}/{l.code}"

    @api.depends('paragraph_id')
    def _get_full_code_label(self):
        for l in self:
            l.display_name = f"{l.paragraph_id.article_id.code}/{l.paragraph_id.code}/{l.code} {l.label}"
