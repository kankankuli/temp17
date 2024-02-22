# -*- coding: utf-8 -*-

##############################################################################
#
#    Weblytic Labs.
#    Copyright (C) 2023 Weblytic Labs (<https://weblyticlabs.com>).
#    Author: WeblyticLabs <support@weblyticlabs.com>
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

{
	'name': 'Built in Calculator for POS',
	'version': '13.0.1.0.0',
	'summary': """The "POS Calculator" is designed to enhance the Point of Sale (POS) system by seamlessly
    integrating a calculator directly into the POS window. With a simple click, users gain access to a
    calculator, streamlining and expediting the calculation process for POS employees.""",
	'description': """The "POS Calculator" app is a revolutionary extension for Odoo ERP, designed to enhance the
    Point of Sale (POS) system by seamlessly integrating a calculator directly into the POS window. With a simple click,
    users gain access to a calculator, streamlining and expediting the calculation process for POS employees.""",
	'category': 'Point of Sale',
	'author': 'Weblytic Labs',
	'company': 'Weblytic Labs',
	'website': "https://store.weblyticlabs.com",
	'depends': ['base', 'point_of_sale', 'mail', 'account', 'sale'],
	'data': [
		'views/pos_config_view.xml',
	],
	'assets': {
		'point_of_sale._assets_pos': [
			'wbl_calculator_in_pos/static/src/app/pos_calculator_button/PosCalculator.js',
			'wbl_calculator_in_pos/static/src/app/pos_calculator_button/PosCalculator.xml',
			'wbl_calculator_in_pos/static/src/app/pos_calculator_popup/PosCalculatorPopup.js',
			'wbl_calculator_in_pos/static/src/app/pos_calculator_popup/PosCalculatorPopup.xml',
			'wbl_calculator_in_pos/static/src/app/pos_calculator_popup/pos_calculator_popup.css',
		],
	},
	'images': ['static/description/banner.gif'],
	'license': 'OPL-1',
	'installable': True,
	'auto_install': False,
	'application': True,
}
