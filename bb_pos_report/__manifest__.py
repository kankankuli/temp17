# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Pos Additional Reports',
    'version': '1.0.1',
    'category': 'Point of Sale',
    'icon': '/bb_pos_report/static/description/icon.png',
    'sequence': 20,
    'author': 'Bayarbayasgalan MGL',
    'summary': 'Point of sale',
    'description': """
This module can show Point of sale addictional report
==============================================
- Pos sale hourly report
- Pos session report
- Pos order all discount calculation
    """,
    # 'price': 2.00,
    # 'currency': 'USD',
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'report/pos_order_report_hour_view.xml',
        'report/pos_session_report_view.xml',
        'report/pos_order_report_discount_view.xml',
    ],
    'qweb': [],
    "images": ["static/description/images/banner.gif","static/description/images/bb_ss1.png","static/description/images/bb_ss2.png","static/description/images/bb_ss3.png"],
    'website': 'https://www.linkedin.com/in/bayarbayasgalan-jagdal/',
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
