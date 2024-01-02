# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    equipment_id = fields.Many2one('equipment', string='Equipment')
    equipment_owner_id = fields.Many2one(related='equipment_id.equipment_owner_id', store=True)
    order_confirmation_date = fields.Datetime(related='order_id.date_order', store=True)

