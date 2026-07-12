from odoo import api, fields, models


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    partner_tags_ids = fields.Many2many(
        comodel_name='res.partner.category',
        string='Partner Tags',
        related='partner_id.category_id',
        readonly=True,
    )
    def action_print_journal_entry(self):
        return self.env.ref('bi_print_journal_entries.journal_entry_report_action').report_action(self)

    def print_report_comp(self):
        if self.cash_type == 'in':
            return self.env.ref('bi_print_journal_entries.report_receipt_voucher_action').report_action(self)
        if self.cash_type == 'out':
            return self.env.ref('bi_print_journal_entries.report_receipt_voucher_action2').report_action(self)

    # add filter for journal entries by account
    account_ids = fields.Many2many(
        'account.account',
        compute='_compute_account_ids',
        store=True,
        string="Accounts",
    )

    @api.depends('line_ids.account_id')
    def _compute_account_ids(self):
        for move in self:
            move.account_ids = move.line_ids.mapped('account_id')
