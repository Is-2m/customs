from odoo import models, fields, api


class Paragraph(models.Model):
    _name = 'finance.paragraph'
    _description = 'Paragraph Description'
    _rec_name = 'label'

    id = fields.Integer(primary_key=True)
    code = fields.Char(required=True, index=True)
    label = fields.Char(required=True)

    article_id = fields.Many2one('finance.article', string='Article', ondelete='cascade')
    ligne_ids = fields.One2many('finance.ligne', 'paragraph_id', string='Lignes')
    full_code = fields.Char(string="Paragraphe", compute="_get_full_code")


    @api.depends('article_id')
    def _get_full_code(self):
        for para in self:
            para.full_code = f"{para.article_id.code}/{para.code}"
