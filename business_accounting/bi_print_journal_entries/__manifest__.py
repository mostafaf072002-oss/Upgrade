# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Print Journal Entries Report in Odoo',
    'version': '14.0.0.0',
    'category': 'Account',
    'summary': 'Allow to print pdf report of Journal Entries.',
    'description': """
    Allow to print pdf report of Journal Entries.
    journal entry
    print journal entry 
    journal entries
    print journal entry reports
    account journal entry reports
    journal reports
    account entry reports

    
""",
    'price': 000,
    'currency': 'EUR',
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.in',
    'depends': ['base', 'account', 'account_dynamic_reports', 'bank_statments_modifications',
                'parallel_account_sequence'],
    'data': [
        # 'report/report_journal_entries.xml',
        'report/report_journal_entries_view.xml',
        'report/report_receipt_voucher.xml',
        'report/report_receipt_voucher2.xml',

        'views/journal_entries_print.xml',

    ],
    'installable': True,
    'auto_install': False,
    'live_test_url': 'https://youtu.be/qehLT4WOWPs',
    "images": ["static/description/Banner.png"],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
