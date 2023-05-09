from odoo import models,fields

class Paragraph(models.Model):
    _name = 'finance.paragraph'
    _description = 'Paragraph Description'
    _rec_name = 'label'

    id = fields.Integer(primary_key=True)
    code = fields.Char(required=True, index=True, unique=True)
    label = fields.Char(required=True)

    article_id = fields.Many2one('finance.article', string='Article', ondelete='cascade')
    ligne_ids = fields.One2many('finance.ligne', 'paragraph_id', string='Lignes')

    def create_ligne(self):
        self.env['finance.ligne'].create({
            'code': 'New Ligne',
            'label': 'New Ligne Label',
            'paragraph_id': self.id
        })