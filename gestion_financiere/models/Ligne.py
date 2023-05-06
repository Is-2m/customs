from odoo import models, fields,api
from odoo.addons.gestion_engagements.models import Engagement


class Ligne(models.Model):
    _name = 'gestion_financiere.ligne'
    _description = 'Ligne Description XD'

    id = fields.Integer(primary_key=True)
    code = fields.Char(required=True, index=True, unique=True)
    label = fields.Char(required=True)
    paragraph_id = fields.Many2one('gestion_financiere.paragraph', string='Paragraph', ondelete='cascade')
    # engagement_ids=fields.One2many("gestion_engagements.engagement","ligne_id",string="Engagements")


    article_code = fields.Char(string='Article Code', compute='_get_article_code', store=False)
    paragraph_code = fields.Char(string='Paragraph Code', compute='_get_paragraph_code', store=False)
    @api.depends('paragraph_id.article_id.code')
    def _get_article_code(self):
        for ligne in self:
            ligne.article_code = ligne.paragraph_id.article_id.code if ligne.paragraph_id and ligne.paragraph_id.article_id else ''

    @api.depends('paragraph_id.code')
    def _get_paragraph_code(self):
        for ligne in self:
            ligne.paragraph_code = ligne.paragraph_id.code if ligne.paragraph_id else ''
