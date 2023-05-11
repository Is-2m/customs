from odoo import models, fields


class Article(models.Model):
    _name = 'finance.article'
    _description = 'Article Description :v'
    _rec_name = 'label'

    id = fields.Integer(primary_key=True)
    code = fields.Char(required=True, index=True)
    label = fields.Char(required=True)

    paragraph_ids = fields.One2many('finance.paragraph', 'article_id', string='Paragraphs')

    _sql_constraints = [
        ('unique_my_field', 'unique(code)', 'My Field must be unique!')
    ]

    def create_paragraph(self):
        self.env['finance.paragraph'].create({
            'code': 'New Paragraph',
            'label': 'New Paragraph Label',
            'article_id': self.id
        })
