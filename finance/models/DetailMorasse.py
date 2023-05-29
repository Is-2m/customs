from docutils.nodes import date
from odoo import fields, models, api


class DetailMorasse(models.Model):
    _name = 'finance.detail_morasse'
    _description = 'lines for morasse'
    # _sql_constraints = [
    #     ('detail_morasse_pk', 'primary key(morasse_id,ligne_id)', '')
    # ]

    id = fields.Id("ID")
    montant = fields.Float('Montant')
    # --------------------------Relations----------------------------------
    morasse_id = fields.Many2one('finance.morasse')
    ligne_id = fields.Many2one('finance.ligne')
    engagement_ids = fields.One2many("finance.engagement", "detail_morasse_id", string="Engagements")

    # -------------------------------- Compute ------------------------------
    morasse_title = fields.Char('Morasse Title', compute='_get_morasse_title', store=True, readonly=True)
    full_line_code_label = fields.Char('Ligne', compute='_get_full_line_code_label', store=False, readonly=True)
    rap = fields.Float("R.A.P", compute="_get_rap", store=False, readonly=False)

    @api.depends('morasse_id')
    def _get_morasse_title(self):
        for d in self:
            d.morasse_title = d.morasse_id.title

    @api.depends('ligne_id')
    def _get_full_line_code_label(self):
        for d in self:
            d.full_line_code_label = f"{d.ligne_id.full_code} {d.ligne_id.label}"

    @api.depends("ligne_id")
    def _get_rap(self):
        for detail in self:
            year = fields.Datetime.today().year
            total_amount = sum(line.montant for line in detail.ligne_id.detail_ids if line.morasse_id.year < year)
            total_paid=sum(op.montant for op in detail.engagement_ids )
            detail.rap = total_amount

# @api.onchange('montant')
# def _regulate_montant(self):
#     for d in self:
# morasse = d.morasse_id
# morasse_total = sum(morasse.detail_ids.mapped('montant'))
# rest =
# if d.montant>:
#     op.montant = 0
# elif op.montant > resting_total:
#     op.montant = resting_total
