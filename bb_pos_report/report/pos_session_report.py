# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class pos_session_report(models.Model):
    _name = "report.pos.session"
    _description = "report pos session"
    _auto = False
    _order = 'start_at desc'

    start_at = fields.Datetime(string='Start Date', readonly=True)
    stop_at = fields.Datetime(string='Closed Date', readonly=True)
    session_id = fields.Many2one('pos.session', string='Session', readonly=True)
    config_id = fields.Many2one('pos.config', string='POS Config', readonly=True)
    user_id = fields.Many2one('res.users', string='Employee', readonly=True)
    cash_register_id = fields.Many2one('account.bank.statement', string='Cash register', readonly=True)
    cash_register_balance_start = fields.Float(
        string="Cash Balance of Start",
        readonly=True)
    cash_register_balance_end_real = fields.Float(
        string="Cash Balance of End",
        readonly=True)
    cash_register_total_entry_encoding = fields.Float(
        string='Total amount of Cash',
        readonly=True,
    )
    cash_register_balance_end = fields.Float(
        string="Must be Cash Balance",
        readonly=True)
    cash_register_difference = fields.Float(
        string='Difference',
        readonly=True)
    bank_amount = fields.Float(string='Bank transaction',
        readonly=True)
    payment_method_id = fields.Many2one('pos.payment.method', string='Payment Method', readonly=True)
    state = fields.Char(string='State', readonly=True)
    total_sale_amount = fields.Float(
        string='Total Sales Amount',
        readonly=True)
    
    total_cash_payment = fields.Float(
        string='Total Cash Amount',
        readonly=True)
    
    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
            select
                id,
                session_id,
                start_at,
                stop_at,
                user_id,
                config_id,
                cash_register_id,
                state,
                payment_method_id,
                sum(cash_register_balance_end_real) as cash_register_balance_end_real,
                sum(cash_register_balance_start) as cash_register_balance_start,
                sum(cash_register_balance_start) + case when state='closed' then sum(total_cash_payment) else sum(total_cash_payment) end+sum(total_entry_encoding) as cash_register_balance_end,
                case when state='closed' then sum(total_cash_payment) else sum(total_cash_payment) end+sum(total_entry_encoding) as cash_register_total_entry_encoding,
                sum(cash_register_balance_end_real)-sum(cash_register_balance_start) + case when state='closed' then sum(total_cash_payment) else sum(total_cash_payment) end+sum(total_entry_encoding) as cash_register_difference,
                sum(bank_amount) as bank_amount,
                sum(total_cash_payment) as total_cash_payment,
                sum(total_sale_amount) as total_sale_amount
                from (
            select
                ps.id as id,
                ps.id as session_id,
                ps.start_at,
                ps.stop_at,
                ps.user_id,
                ps.config_id,
                ps.cash_register_id,
                ps.state,
                abs.balance_end_real as cash_register_balance_end_real,
                abs.balance_start as cash_register_balance_start,
                0 as cash_register_balance_end,
                abs.total_entry_encoding as total_entry_encoding,
                0 as total_cash_payment,
                0 as cash_register_difference,
                null as payment_method_id,
                0 as bank_amount,
                0 as total_sale_amount
            from
                pos_session ps
            left join account_bank_statement abs on (abs.id=ps.cash_register_id)
            where ps.cash_register_id is not null
            union all
            select
                pp.id as id,
                ps.id as session_id,
                ps.start_at,
                ps.stop_at,
                ps.user_id,
                ps.config_id,
                ps.cash_register_id,
                ps.state,
                0 as cash_register_balance_end_real,
                0 as cash_register_balance_start,
                0 as cash_register_balance_end,
                0 as total_entry_encoding,
                case when ppm.is_cash_count = true then pp.amount else 0 end as total_cash_payment,
                0 as cash_register_difference,
                pp.payment_method_id,
                case when ppm.is_cash_count = false then pp.amount else 0 end as bank_amount,
                0 as total_sale_amount
            from pos_payment pp
            left join pos_session ps on (ps.id=pp.session_id)
            left join pos_payment_method ppm on (ppm.id=pp.payment_method_id)
            where ps.cash_register_id is not null
            union all
            select
                po.id as id,
                ps.id as session_id,
                ps.start_at,
                ps.stop_at,
                ps.user_id,
                ps.config_id,
                ps.cash_register_id,
                ps.state,
                0 as cash_register_balance_end_real,
                0 as cash_register_balance_start,
                0 as cash_register_balance_end,
                0 as total_entry_encoding,
                0 as total_cash_payment,
                0 as cash_register_difference,
                null as payment_method_id,
                0 as bank_amount,
                sum(amount_total) as total_sale_amount
            from pos_order po
            left join pos_session ps on (ps.id=po.session_id)
            where ps.cash_register_id is not null
            group by 1,2,3,4,5,6,7,8,9
            ) as temp_sess_haalt
            group by
            id,
                session_id,
                start_at,
                stop_at,
                user_id,
                config_id,
                cash_register_id,
                state,
                payment_method_id
            )
        """ % (self._table)
        )