# Copyright 2018 Xavier Piernas <xavier.piernas@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def bank_accounts_report(self):
        bank_accounts = []
        if self.payment_mode_id:
            if self.payment_mode_id.account_source == 'company':
                if self.payment_mode_id.invoice_account and\
                        self.partner_bank_id:
                    bank_accounts.append(self.partner_bank_id)
                elif self.payment_mode_id.res_partner_bank_ids:
                    for account in self.payment_mode_id.res_partner_bank_ids:
                        bank_accounts.append(account)
            if self.payment_mode_id.account_source == 'partner':
                if self.mandate_required and self.mandate_id and\
                        self.mandate_id.partner_bank_id:
                    bank_accounts.append(self.mandate_id.partner_bank_id)
                else:
                    if self.payment_mode_id.\
                            partner_account_source == 'mandate':
                        mandates = self.partner_id.commercial_partner_id.\
                            sdd_mandate_ids.filtered(
                                lambda x: x.state == 'active'and
                                x.partner_bank_id
                            )
                        if mandates:
                            bank_accounts.append(mandates[-1].partner_bank_id)
                    else:
                        accounts = self.partner_id.commercial_partner_id.\
                            bank_ids
                        if accounts:
                            bank_accounts.append(accounts[-1])
        return bank_accounts
