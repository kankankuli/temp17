# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools

class PosOrderReportHour(models.Model):
    _name = "report.pos.order.hour"
    _description = "report.pos.order.hour"
    
    dy = fields.Selection(
        selection=[('mon', u'Monday'),
                    ('tue', u'Tuesday'),
                    ('wed', u'Wednesday'),
                    ('thu', u'Thursday'),
                    ('fri', u'Friday'),
                    ('sat', u'Saturday'),
                    ('sun', u'Sunday'),
                    ],string='Day')

class PosOrderReport(models.Model):
    _inherit = "report.pos.order"
    
    dy = fields.Selection(
        selection=[('mon', u'Monday'),
                    ('tue', u'Tuesday'),
                    ('wed', u'Wednesday'),
                    ('thu', u'Thursday'),
                    ('fri', u'Friday'),
                    ('sat', u'Saturday'),
                    ('sun', u'Sunday'),
                    ],string='Day')
    hour = fields.Char('Hour', readonly=True)

    def _select(self):
        res = super(PosOrderReport, self)._select()
        res+="""
        ,
        to_char((s.date_order + interval '8 hour'), 'dy') as dy,
        EXTRACT(hour from (s.date_order + interval '8 hour')) as hour
        """
        return res
