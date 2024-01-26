# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools

class pos_order_report_discount(models.Model):
    _name = "report.pos.report.discount"
    _description = "report pos order discount"
    _auto = False
    _order = 'date desc'

    date = fields.Datetime(string='Order Date', readonly=True)
    order_id = fields.Many2one('pos.order', string='Order', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('paid', 'Paid'), ('done', 'Done'),
         ('invoiced', 'Invoiced'), ('cancel', 'Cancel')],
        string='State')
    user_id = fields.Many2one('res.users', string='Cashier', readonly=True)
    price_total = fields.Float(string='Total Sales Amount', readonly=True)
    
    total_discount = fields.Float(string='Total Discount', readonly=True)
    total_discount_price = fields.Float(string='Discount', readonly=True)
    total_discount_card = fields.Float(string='Card Discount /with Partner/', readonly=True)
    
    average_price = fields.Float(string='Average Price', readonly=True, group_operator="avg")
    location_id = fields.Many2one('stock.location', string='Location', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    nbr_lines = fields.Integer(string='Lines count', readonly=True)
    product_qty = fields.Integer(string='Count', readonly=True)
    product_categ_id = fields.Many2one('product.category', string='Category', readonly=True)
    invoiced = fields.Boolean(readonly=True, string='to Invoice')
    config_id = fields.Many2one('pos.config', string='POS Config', readonly=True)
    pos_categ_id = fields.Many2one('pos.category', string='POS Category', readonly=True)
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', readonly=True)
    session_id = fields.Many2one('pos.session', string='Session', readonly=True)
    
    list_price = fields.Float(string='Main unit prce', readonly=True, group_operator="avg")
    default_code = fields.Char(string='Default code', readonly=True)
    barcode = fields.Char(string='Barcode', readonly=True)
    
    def _select(self):
        return """
            SELECT
                l.id AS id,
                1 AS nbr_lines,
                s.date_order AS date,
                l.qty AS product_qty,
                ((l.qty * l.price_unit) * (100 - l.discount) / 100 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS price_total,
                ((l.qty * (CASE WHEN l.list_price IS NULL THEN pt.list_price ELSE pt.list_price END) / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) - ((l.qty * l.price_unit) * (100 - l.discount) / 100 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)) as total_discount,
                ((l.qty*l.price_unit / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)/(l.qty * u.factor))::decimal AS average_price,
                s.id as order_id,
                
                CASE WHEN s.partner_id is not null THEN ((l.qty * (CASE WHEN l.list_price IS NULL THEN pt.list_price ELSE pt.list_price END) / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) - ((l.qty * l.price_unit) * (100 - l.discount) / 100 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)) ELSE 0 END as total_discount_card,
                0 as total_discount_price,
                s.partner_id AS partner_id,
                s.state AS state,
                s.user_id AS user_id,
                s.location_id AS location_id,
                s.company_id AS company_id,
                s.sale_journal AS journal_id,
                l.product_id AS product_id,
                pt.categ_id AS product_categ_id,
                p.product_tmpl_id,
                ps.config_id,
                pt.pos_categ_id,
                s.pricelist_id,
                s.session_id,
                s.account_move IS NOT NULL AS invoiced,
                
                p.default_code,
                p.barcode,
                (CASE WHEN l.list_price IS NULL THEN pt.list_price ELSE pt.list_price END) as list_price

        """

    def _from(self):
        return """
            FROM pos_order_line AS l
                INNER JOIN pos_order s ON (s.id=l.order_id)
                LEFT JOIN product_product p ON (l.product_id=p.id)
                LEFT JOIN product_template pt ON (p.product_tmpl_id=pt.id)
                LEFT JOIN uom_uom u ON (u.id=pt.uom_id)
                LEFT JOIN pos_session ps ON (s.session_id=ps.id)
        """

    def _group_by(self):
        return """
            
        """

    def _where(self):
        return """
            where
                l.qty != 0
        """

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s
                %s
            )
        """ % (self._table, self._select(), self._from(), self._group_by(),self._where())
        )