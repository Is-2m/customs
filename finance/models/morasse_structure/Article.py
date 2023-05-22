from odoo import models, fields, api


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
        codei = self.env.context.get('codei')
        labeli = self.env.context.get('labeli')
        # print(codei)
        # print("label")
        # print(labeli)
        self.env['finance.paragraph'].create({
            'code': codei,
            'label': labeli,
            'article_id': self.id
        })

    # @api.model
    # def create_graph(self, code, label):
    #     fields.Command.create({
    #
    #     })

        # self.env['finance.paragraph'].create({
        #     'code': code,
        #     'label': label,
        #     'article_id': self.id
        # })
