from odoo import models, fields, api


class Article(models.Model):
    _name = 'finance.article'
    _description = 'Article Description :v'
    _rec_name = 'label'

    id = fields.Integer(primary_key=True)
    code = fields.Char(required=True, index=True)
    label = fields.Char(required=True)

    paragraph_ids = fields.One2many('finance.paragraph', 'article_id', string='Paragraphs')