# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2014 Tech Receptives (<http://techreceptives.com>)

{
    'name': 'Malaysia - Accounting - Trading Company',
    'author': 'Qten Computer',
    'version': '1.0.0',
    'summary': """Chart of Account Malaysia""",
    'website': 'https://www.qtencomputer.com',
    'category': 'Localization',
    'license': 'LGPL-3',
    'description': """
Malaysia Chart of Accounts for Trading Company.
=======================================================

This module Install The Chart of Accounts of Malaysia, including SST and GST code, for Trading Company.


    """,
    'images' : ['static/src/img/banner.jpg'],
    'depends': ['base', 'account'],
    'data': [
        'data/l10n_my_chart_data.xml',
        'data/account_data.xml',
        'data/account_tax_data.xml',
        'data/account_chart_template_data.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
   
}
