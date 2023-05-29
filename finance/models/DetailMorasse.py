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
            total_previous_lines = sum(line.montant for line in detail.ligne_id.detail_ids if line.morasse_id.year < year)
            detail.rap = total_previous_lines - self.sum_previous_ops()

    def sum_of_current_ops(self):
        total_op = 0
        query = f'''
                    select sum(op.montant) from finance_ordre_payment op
                    join finance_bon_commande bc on bc.id = op.bon_com_id
                    join finance_detail_morasse dm on dm.id = bc.detail_morasse_id
                    join finance_morasse mrs ON mrs.id = dm.morasse_id
                    where dm.ligne_id={self.ligne_id}
                    and mrs."year"={self.morasse_id.year};
                '''

    def sum_previous_ops(self):
        total_op = 0
        query = f'''
                    select sum(op.montant) from finance_ordre_payment op
                    join finance_bon_commande bc on bc.id = op.bon_com_id
                    join finance_detail_morasse dm on dm.id = bc.detail_morasse_id
                    join finance_morasse mrs ON mrs.id = dm.morasse_id
                    where dm.ligne_id={self.ligne_id}
                    and mrs."year"<{self.morasse_id.year};
                '''
        self.env.cr.execute(query)
        result = self.env.cr.fetchone()
        if result:
            total_op = result
        return total_op

    def sum_previous_lines(self):
        detail_morasse = self.env['finance.detail_morasse']
        montant_sum = detail_morasse.search([
            ('ligne_id', '=', self.ligne_id),
            ('morasse_id.year', '<', self.morasse_id.year)
        ]).mapped('montant')

        total_montant = sum(montant_sum)
        return total_montant

    # sum of a year's recette
    def sum_of_recette(self):
        total_recette = 0
        query = f'''
                select sum(montant_chiffre) from finance_ordre_recette
                where "year" ={self.morasse_id.year};
            '''
        self.env.cr.execute(query)
        result = self.env.cr.fetchone()
        if result:
            total_recette = result
        return total_recette

    @api.onchange('montant')
    def _regulate_montant(self):
        recette_total = self.sum_of_recette()
        for d in self:
            morasse = d.morasse_id
            morasse_total = sum(morasse.detail_ids.mapped('montant'))
            rest = recette_total - morasse_total
            if rest == 0:
                d.montant = 0
            elif d.montant > rest:
                d.montant = rest
