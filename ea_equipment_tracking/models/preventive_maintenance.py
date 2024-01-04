# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PreventiveMaintenance(models.Model):
    _name = 'preventive.maintenance'
    _description = 'Preventive maintenance for Equipment'
    _order = 'commenced_on desc'
    _inherit = ['mail.thread']

    name = fields.Char('Preventive Maintenance', required=True, copy=False, track_visibility='on_change')
    equipment_owner_id = fields.Many2one('equipment.owner', required=True, string='Equipment Owner', track_visibility='on_change')
    location_id = fields.Many2one('customer.location', string='Location', required=True, track_visibility='on_change')
    equipment_category_id = fields.Many2one('equipment.category', string='Equipment Category', required=True, track_visibility='on_change')
    commenced_on = fields.Date('Date Started', required=True, track_visibility='on_change')
    date_ended = fields.Date('Date Finished', track_visibility='on_change')
    next_pm_date = fields.Date('Next Maintenance', track_visibility='on_change')
    equipment_lines_options = fields.One2many('pm.lines', 'equipment_lines', string='Serviced Equipment', track_visibility='on_change')

#         Method to allow the duplicating as 'name' cannot be copied
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of [{}%]".format(self.name))])
        if not copied_count:
            new_name = u"Copy of [{}]".format(self.name)
        else:
            new_name = u"Copy of [{}] ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(PreventiveMaintenance, self).copy(default)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Error! Preventive Maintenance title already exists!"),
        ('next_pm_date_greater_1', 'check(next_pm_date > commenced_on)',
         'Error! Next Preventive Maintenance Date should be later than the Current Start Date!'),
        ('next_pm_date_greater_2', 'check(next_pm_date > date_ended)',
         'Error! Next Preventive Maintenance Date should be later than the Current End Date'),
        ('end_date_greater', 'check(date_ended >= commenced_on)',
         'Error! Preventive maintenance End Date should be later than the Start Date'),
    ]


class PmLines(models.Model):
    _name = 'pm.lines'

    equipment_lines = fields.Many2one('preventive.maintenance', string='Serviced Equipment')
    equipment_id = fields.Many2one('equipment', string='Equipment', required=True)
    where_installed = fields.Many2one(related='equipment_id.where_installed', string='Place Installed')
    equipment_owner_id = fields.Many2one(related='equipment_id.equipment_owner_id', string='Equipment Owner')
    service_date = fields.Date('Date of Service')
    service_done = fields.Char('Service Done')
    reference = fields.Char('Reference')
    equipment_status = fields.Selection([('excellent','Excellent'),
                                         ('average', 'Average'),
                                         ('below_average', 'Below Average'),
                                         ('not_working', 'Not Working'),], string='Equipment Status')
    remarks = fields.Char('Remarks')
