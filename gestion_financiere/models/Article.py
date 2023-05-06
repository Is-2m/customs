from odoo import models, fields

class Article(models.Model):
    _name = 'gestion_financiere.article'
    _description = 'Article Description :v'

    id = fields.Integer(primary_key=True)
    code = fields.Char(required=True, index=True, unique=True)
    label = fields.Char(required=True)

    paragraph_ids = fields.One2many('gestion_financiere.paragraph', 'article_id', string='Paragraphs')

    def create_paragraph(self):
        self.env['gestion_financiere.paragraph'].create({
            'code': 'New Paragraph',
            'label': 'New Paragraph Label',
            'article_id': self.id
        })

