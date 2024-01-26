# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from datetime import timedelta
import time
import pytz
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError,ValidationError
from odoo.http import request
import json, requests
import psycopg2

class PosOrderLine(models.Model):
    _inherit = "pos.order.line"
    
    list_price = fields.Float('List price')
    price_dirty_subtotal = fields.Float(compute='_compute_amount_line_dirty', digits=0, string='Cross sales amount')
    price_dirty_discount = fields.Float(compute='_compute_amount_line_dirty', digits=0, string='Cross discount')
    
    def get_oline_list_price(self, line):
        product = self.env['product.product'].browse(line[2]['product_id'])
        return product.list_price
        
    def _order_line_fields(self, line, session_id=None):
        order_line_fields = super(PosOrderLine, self)._order_line_fields(line, session_id)
        order_line_fields[2]['list_price'] = self.get_oline_list_price(line)
        return order_line_fields

    @api.depends('price_unit', 'tax_ids', 'qty', 'discount', 'product_id','price_subtotal_incl')
    def _compute_amount_line_dirty(self):
        for line in self:
            line.update({
                'price_dirty_subtotal': line.qty*line.list_price,
                'price_dirty_discount': line.qty*line.list_price-line.price_subtotal_incl,
            })
