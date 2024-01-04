# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _


class EquipmentCategory(models.Model):
    _name = 'equipment.category'
    _description = 'Equipment Category'
    _inherit = ['mail.thread']

    name = fields.Char(string='Category Name', required=True)
    maintenance_team_id = fields.Many2one(
        'maintenance.team', string='Maintenance Team')
    note = fields.Text('Notes')
    active = fields.Boolean(default=True, track_visibility='onchange')

    equipment_ids = fields.One2many(
        'equipment', 'category_id', copy=False, string='Equipment')
    equipment_count = fields.Integer(
        compute='_compute_equipment_count', string='Equipment')
    ticket_ids = fields.One2many(
        'maintenance.ticket', 'category_id', copy=False, string='Maintenance Issues')
    ticket_count = fields.Integer(
        compute='_compute_ticket_count', string='Tickets')

    _sql_constraints = [('category_name_unique', 'unique(name)',
                         'Equipment Category Name already exists!')]

    def _compute_equipment_count(self):
        equipment_data = self.env['equipment'].read_group(
            [('category_id', 'in', self.ids)], ['category_id'], ['category_id'])
        mapped_data = dict(
            [(m['category_id'][0], m['category_id_count']) for m in equipment_data])
        for category in self:
            category.equipment_count = mapped_data.get(category.id, 0)

    def _compute_ticket_count(self):
        maintenance_data = self.env['maintenance.ticket'].read_group(
            [('category_id', 'in', self.ids)], ['category_id'], ['category_id'])
        mapped_data = dict(
            [(m['category_id'][0], m['category_id_count']) for m in maintenance_data])
        for category in self:
            category.ticket_count = mapped_data.get(category.id, 0)


class MaintenanceTeam(models.Model):
    _name = 'maintenance.team'
    _description = 'Equipment Maintenance Team'
    _inherit = ['mail.thread']

    name = fields.Char('Maintenance Team Name', required=True)
    team_leader_id = fields.Many2one(
        'res.users', string='Team Leader', required=True)
    team_member_ids = fields.Many2many(
        'res.users', string='Team Members', required=True)
    ticket_ids = fields.One2many('maintenance.ticket', 'responsible_team_id', copy=False, string='Tickets')
    tickets_count = fields.Integer(
        compute='_compute_tickets_count', string='Tickets')
    active = fields.Boolean(default=True, track_visibility='onchange')

    _sql_constraints = [('team_name_unique', 'unique(name)',
                         'Maintenance Team already exists!')]

    # For equipment kanban view
    tickets_in_progress = fields.Integer(
        compute='_compute_tickets_in_progress')

    @api.depends('ticket_ids')
    def _compute_tickets_in_progress(self):
       # self.ensure_one()
        self.tickets_in_progress = len(self.ticket_ids.filtered(
            lambda x: x.state in ['assigned', 'in_progress', 'resolved']))

    def _compute_tickets_count(self):
        tickets_data = self.env['maintenance.ticket'].read_group([('responsible_team_id', 'in', self.ids)],
                                                                 ['responsible_team_id'], ['responsible_team_id'])
        mapped_data = dict(
            [(m['responsible_team_id'][0], m['responsible_team_id_count']) for m in tickets_data])
        for team in self:
            team.tickets_count = mapped_data.get(team.id, 0)


class EquipmentOwner(models.Model):
    _name = 'equipment.owner'
    _description = 'Maintenance Customer'
    _inherit = ['mail.thread']

    name = fields.Char(related='partner_id.name', string='Equipment Owner')
    partner_id = fields.Many2one('res.partner', string='Related Partner')
    phone = fields.Char(related='partner_id.phone', string='Landline')
    mobile = fields.Char(related='partner_id.mobile', string='Mobile')
    email = fields.Char(related='partner_id.email', string='Email')
    active = fields.Boolean(default=True, track_visibility='onchange')
    color = fields.Integer('Color Index')

    equipment_ids = fields.One2many(
        'equipment', 'equipment_owner_id', copy=False, string='Equipment')
    ticket_ids = fields.One2many(
        'maintenance.ticket', 'equipment_owner_id', copy=False, string='Tickets')

    # For the Smart Buttons in the Equipment Owner Form
    equipment_count = fields.Integer(
        compute='_compute_equipment_count', string='Equipment')
    tickets_count = fields.Integer(
        compute='_compute_tickets_count', string='Tickets')

    # # For the Equipment Owners Dashboard
    # new_tickets = fields.Integer(compute='_compute_tickets')
    tickets_in_progress = fields.Integer(compute='_compute_tickets')

    @api.depends('ticket_ids')
    def _compute_tickets(self):
       # self.ensure_one()
        self.tickets_in_progress = len(self.ticket_ids.filtered(
            lambda x: x.state not in ['cancelled', 'closed']))

    _sql_constraints = [('equipment_owner_name_unique',
                         'unique(name)', 'Equipment Owner already exists!')]

    def _compute_equipment_count(self):
        equipment_data = self.env['equipment'].read_group([('equipment_owner_id', 'in', self.ids)], ['equipment_owner_id'],
                                                          ['equipment_owner_id'])
        mapped_data = dict(
            [(m['equipment_owner_id'][0], m['equipment_owner_id_count']) for m in equipment_data])
        for owner in self:
            owner.equipment_count = mapped_data.get(owner.id, 0)

    def _compute_tickets_count(self):
        tickets_data = self.env['maintenance.ticket'].read_group(
            [('equipment_owner_id', 'in', self.ids)], ['equipment_owner_id'], ['equipment_owner_id'])
        mapped_data = dict(
            [(m['equipment_owner_id'][0], m['equipment_owner_id_count']) for m in tickets_data])
        for owner in self:
            owner.tickets_count = mapped_data.get(owner.id, 0)


class CustomerLocation(models.Model):
    _name = 'customer.location'
    _description = 'Customer Location'

    name = fields.Char('Customer Location', required=True)
    equipment_owner_id = fields.Many2one(
        'equipment.owner', required=True, string='Equipment Owner')
    active = fields.Boolean(default=True, track_visibility='onchange')

    equipment_ids = fields.One2many(
        'equipment', 'location', copy=False, string='Equipment')
    equipment_count = fields.Integer(
        compute='_compute_equipment_count', string='Equipment')

    def _compute_equipment_count(self):
        equipment_data = self.env['equipment'].read_group([('location', 'in', self.ids)],
                                                          ['location'],
                                                          ['location'])
        mapped_data = dict([(m['location'][0], m['location_count'])
                            for m in equipment_data])
        for location in self:
            location.equipment_count = mapped_data.get(location.id, 0)


class PlaceInstalled(models.Model):
    _name = 'place.installed'
    _description = 'Equipment Installation Area'

    name = fields.Char('Place', required=True)
    equipment_owner_id = fields.Many2one(
        'equipment.owner', string='Equipment Owner', required=True)
    location_id = fields.Many2one(
        'customer.location', required=True, string='Location')
