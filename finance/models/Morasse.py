from odoo import fields, models, api


class Morasse(models.Model):
    _name = 'finance.morasse'
    # _description = 'Description'
    _rec_name = 'title'
    _sql_constraints = [
        ('unique_morasse_year', 'unique(year)', 'L\'année de morasse doit être unique!')
    ]

    year = fields.Integer("Année", default=lambda self: fields.Datetime.today().year, required=True)
    # -------------------------- Relations ---------------------------------
    detail_ids = fields.One2many('finance.detail_morasse', 'morasse_id')
    display_name = fields.Char(compute="_compute_display_name")
    # -------------------------- Computed ----------------------------------
    title = fields.Char(compute='_compute_display_name', store=True)
    commaless_year = fields.Char('Année', compute='_year_as_char', store=False)

    @api.depends('year')
    def _compute_display_name(self):
        for o in self:
            o.title = f'Morasse {o.year}'
            o.display_name=f'Morasse {o.year}'
    @api.depends('year')
    def _year_as_char(self):
        for m in self:
            m.commaless_year = '{:04d}'.format(m.year)
