from odoo import models,fields

class Paragraph(models.Model):
    _name = 'gestion_financiere.paragraph'
    _description = 'Paragraph Description :3'

    id = fields.Integer(primary_key=True)
    code = fields.Char(required=True, index=True, unique=True)
    label = fields.Char(required=True)

    article_id = fields.Many2one('gestion_financiere.article', string='Article', ondelete='cascade')
    ligne_ids = fields.One2many('gestion_financiere.ligne', 'paragraph_id', string='Lignes')

    def create_ligne(self):
        self.env['gestion_financiere.ligne'].create({
            'code': 'New Ligne',
            'label': 'New Ligne Label',
            'paragraph_id': self.id
        })