# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from pprint import pprint


class Equipment(models.Model):
    _name = 'equipment'
    _description = 'Equipment'
    _inherit = ['mail.thread']
    name = fields.Char('Serial Number', track_visibility='onchange', required=True, copy=False,
                       help='Main ID used by Equipment Owner')
    category_id = fields.Many2one('equipment.category', required=True, string='Equipment Category')
    equipment_owner_id = fields.Many2one('equipment.owner', string='Equipment Owner', track_visibility='onchange')
    tag_id_number = fields.Char('Alternative ID #', track_visibility='onchange')
    location = fields.Many2one('customer.location', string='Equipment Location', track_visibility='onchange')
    where_installed = fields.Many2one('place.installed', string='Where Installed', track_visibility='onchange')
    notes = fields.Text('Additional Notes', copy=False)
    make = fields.Char('Make', track_visibility='onchange')
    model = fields.Char('Model', track_visibility='onchange')
    capacity = fields.Char('Capacity')
    active = fields.Boolean(default=True, track_visibility='onchange')

    ticket_ids = fields.One2many('maintenance.ticket', 'equipment_id', copy=False, string='Tickets')
    tickets_count = fields.Integer(compute='_compute_tickets_count', string='Tickets')

    order_line_ids = fields.One2many('sale.order.line', 'equipment_id', copy=False, string='Order Lines')
    order_line_count = fields.Integer(compute='_compute_order_line_count', string='Cost Items')
    order_line_total = fields.Float(compute='_compute_order_line_total', string='Total Cost')

    pm_line_ids = fields.One2many('pm.lines', 'equipment_id', copy=False, string='Preventive Maintenance')
    pm_count = fields.Integer(compute='_compute_pm_count', string='Preventive Maintenance')

    # For equipment kanban view
    tickets_in_progress = fields.Integer(compute='_compute_tickets_in_progress')

    @api.depends('order_line_ids.price_subtotal')
    def _compute_order_line_total(self):
        for cost in self:
            total = 0.0
            for line in cost.order_line_ids:
                if line.state == 'sale':
                    total += line.price_subtotal
            cost.update({'order_line_total': total})

    @api.depends('ticket_ids')
    def _compute_tickets_in_progress(self):
        # self.ensure_one()
        self.tickets_in_progress = len(self.ticket_ids.filtered(lambda x: x.state not in ['closed', 'cancelled']))

    @api.depends('order_line_ids')
    def _compute_order_line_count(self):
        # self.ensure_one()
        self.order_line_count = len(self.order_line_ids.filtered(lambda x: x.state in ['sale', 'done']))

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Equipment Serial Number already exists !"),
        ('tag_uniq', 'unique (tag_id_number)', "Tag ID Number already exists !"),
    ]

    def _compute_tickets_count(self):
        tickets_data = self.env['maintenance.ticket'].read_group([('equipment_id', 'in', self.ids)],
                                                                 ['equipment_id'], ['equipment_id'])
        mapped_data = dict([(m['equipment_id'][0], m['equipment_id_count']) for m in tickets_data])
        pprint(tickets_data)
        for equipment in self:
            equipment.tickets_count = mapped_data.get(equipment.id, 0)

    def _compute_pm_count(self):
        pm_data = self.env['pm.lines'].read_group([('equipment_id', 'in', self.ids)],
                                                                 ['equipment_id'], ['equipment_id'])
        mapped_data = dict([(m['equipment_id'][0], m['equipment_id_count']) for m in pm_data])
        for equipment in self:
            equipment.pm_count = mapped_data.get(equipment.id, 0)

#         Method to allow the duplicate function as 'name' cannot be copied

    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of [{}%]".format(self.name))])
        if not copied_count:
            new_name = u"Copy of [{}]".format(self.name)
        else:
            new_name = u"Copy of [{}] ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Equipment, self).copy(default)
