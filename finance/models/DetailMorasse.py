from odoo import fields, models, api


class DetailMorasse(models.Model):
    _name = 'finance.detail_morasse'
    _description = 'lines for morasse'
    _rec_name = "display_name"
    _sql_constraints = [
        ('unique_morasse_ligne', 'unique (morasse_id,ligne_id)',
         'cette ligne est déjà alimentée dans cette morasse.'
         + ' veuillez choisir une autre ligne, ou si vous voulez changer son montant éditez celui existant')
    ]

    id = fields.Id("ID")
    montant = fields.Float('Montant')
    # --------------------------Relations----------------------------------
    morasse_id = fields.Many2one('finance.morasse', default=lambda self: self._default_morasse_id())
    ligne_id = fields.Many2one('finance.ligne')
    engagement_ids = fields.One2many("finance.engagement", "detail_morasse_id", string="Engagements")

    # -------------------------------- Computed ------------------------------
    morasse_title = fields.Char('Morasse Title', compute='_get_morasse_title', store=True, readonly=True)
    full_line_code_label = fields.Char('Ligne', compute='_get_full_line_code_label', store=False, readonly=True)
    rap = fields.Float("R.A.P", compute="_get_rap", store=False, readonly=False)
    total_recette = fields.Float(compute="sum_of_recette", readonly=True)
    rest_recette = fields.Float(compute="get_rest_recette", readonly=True)
    display_name = fields.Char(compute="_get_display_name")

    @api.depends('ligne_id', 'morasse_id')
    def _get_display_name(self):
        for detail in self:
            detail.display_name = f'{detail.ligne_id.display_name} - {detail.morasse_id.display_name}'

    @api.model
    def _default_morasse_id(self):
        current_year = fields.datetime.now().year
        morasse_id = self.env['finance.morasse'].search([('year', '=', current_year)], limit=1)
        return morasse_id

    @api.depends("montant", 'morasse_id')
    def get_rest_recette(self):
        for detail in self:
            recette_total = detail.sum_of_recette()
            morasse = detail.morasse_id
            morasse_total = sum(morasse.detail_ids.mapped('montant'))
            rest = recette_total - morasse_total
            detail.rest_recette = rest
            return rest

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
            year = detail.morasse_id.year
            total_previous_lines = \
                sum(line.montant for line in detail.ligne_id.detail_ids if line.morasse_id.year < year)
            detail.rap = total_previous_lines - detail.sum_previous_ops()

    def sum_of_current_ops(self):
        total_op = 0
        for detail in self:
            query = f'''
                                select sum(op.montant) from finance_ordre_payment op
                                join finance_bon_commande bc on bc.id = op.bon_com_id
                                join finance_detail_morasse dm on dm.id = bc.detail_morasse_id
                                join finance_morasse mrs ON mrs.id = dm.morasse_id
                                where dm.ligne_id={detail.ligne_id.id}
                                and mrs."year"={detail.morasse_id.year};
                            '''

    # used to calculate the R.A.P
    def sum_previous_ops(self):
        total_op = 0
        for detail in self:
            query = f'''
                        select sum(op.montant) from finance_ordre_payment op
                        join finance_bon_commande bc on bc.id = op.bon_com_id
                        join finance_detail_morasse dm on dm.id = bc.detail_morasse_id
                        join finance_morasse mrs ON mrs.id = dm.morasse_id
                        where dm.ligne_id={detail.ligne_id.id}
                        and mrs."year"<{detail.morasse_id.year};
                    '''
            self.env.cr.execute(query)
            result = self.env.cr.fetchone()
            if result[0]:
                total_op = result[0]
            return total_op

    def sum_previous_lines(self):
        detail_morasse = self.env['finance.detail_morasse']
        for detail in self:
            montant_sum = detail_morasse.search([
                ('ligne_id', '=', detail.ligne_id),
                ('morasse_id.year', '<', detail.morasse_id.year)
            ]).mapped('montant')
            total_montant = sum(montant_sum)
            return total_montant

    # sum of some year's recette
    def sum_of_recette(self):
        total_recette = 0
        for detail in self:
            query = f'''
                    select sum(montant_chiffre) from finance_ordre_recette
                    where "year" ={detail.morasse_id.year};
                '''
            self.env.cr.execute(query)
            result = self.env.cr.fetchone()
            if result[0]:
                total_recette = result[0]
            detail.total_recette = total_recette
            return total_recette

    @api.onchange('montant')
    def _regulate_montant(self):
        for d in self:
            rest = d.get_rest_recette()
            if rest == 0:
                d.montant = 0
            elif d.montant > rest:
                d.montant = rest
