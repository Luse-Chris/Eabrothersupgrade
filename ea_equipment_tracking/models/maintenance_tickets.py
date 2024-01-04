# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _


class MaintenanceTicket(models.Model):
    _name = 'maintenance.ticket'
    _description = 'Maintenance Ticket for Equipment'
    _order = 'name desc'
    _inherit = ['mail.thread']

    name = fields.Char('Maintenance Ticket', copy=False, default=lambda self: ('New'), readonly=True)
    subject = fields.Char('Maintenance Subject', required=True, track_visibility='onchange')
    equipment_id = fields.Many2one('equipment', string='Affected Equipment', track_visibility='onchange', copy=False)
    tag_id_number = fields.Char(related='equipment_id.tag_id_number', store=True, copy=False)
    category_id = fields.Many2one(related='equipment_id.category_id', string='Category', store=True)
    serial_number = fields.Char(related='equipment_id.name', string='Serial Number', readonly=True, store=True)
    equipment_owner_id = fields.Many2one(related='equipment_id.equipment_owner_id', track_visibility='onchange', store=True)
    location = fields.Many2one(related='equipment_id.location', store=True)
    where_installed = fields.Many2one(related='equipment_id.where_installed', store=True)
    reported_by_name = fields.Char('Reported by', required='True', track_visibility='onchange')
    reported_by_phone = fields.Char('Phone / Email', track_visibility='onchange')
    customer_ref = fields.Char('Customer Reference', copy=False)
    reporting_date = fields.Date('Date Reported', track_visibility='onchange', required=True)
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority',
                                track_visibility='onchange')
    responsible_team_id = fields.Many2one('maintenance.team', string='Responsible Team', track_visibility='onchange', copy=False)
    assigned_to_id = fields.Many2one('hr.employee', string='Assigned To', track_visibility='onchange', copy=False)
    assigned_to_email = fields.Char(related='assigned_to_id.work_email', store=True)
    assigned_date = fields.Date('Assigned Date', track_visibility='onchange', index=True, readonly=True, copy=False)
    scheduled_date = fields.Date('Scheduled Date', track_visibility='onchange', copy=False)
    date_in_progress = fields.Date(string='Started Work on', copy=False, readonly=True, track_visibility='onchange')
    date_resolved = fields.Date(string='Date Resolved', copy=False, readonly=True, track_visibility='onchange')
    # close_date = fields.Date(string='Close Date', copy=False, readonly=True, track_visibility='onchange')
    close_date = fields.Date('Close Date', track_visibility='onchange', index=True, readonly=True, copy=False)
    description = fields.Text('Description', copy=False)
    summary_resolution = fields.Char('Summary Resolution', copy=False)
    resolution = fields.Text('Problem Resolution', copy=False)
    remarks = fields.Text('Remarks', copy=False)
    state = fields.Selection([
        ('new', "New"),
        ('approved', "Approved"),
        ('assigned', "Assigned"),
        ('in_progress', "In Progress"),
        ('resolved', "Resolved"),
        ('closed', "Closed"),
        ('cancelled', "Cancelled")], default='new', track_visibility='onchange')
    created_by_id = fields.Many2one('hr.employee', string='Created by',
                                    default=lambda self: self.env['hr.employee'].search(
                                        [('user_id', '=', self.env.uid)], limit=1))
    url = fields.Char('Url')

#     Constraint to ensure scheduled_date not less than reporting_date
    _sql_constraints = [
        ('scheduled_date_greater', 'check(reporting_date <= scheduled_date)',
         'Error ! The date the maintenance is to be carried out cannot be earlier than the date the issue was reported.'),
        ('close_date_greater', 'check(close_date >= reporting_date)',
         'Error ! Closing date cannot be earlier than the day the issue was reported.')
        ]

    @api.model
    def create(self, vals):
        if 'name' not in vals or vals['name'] == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.ticket') or ('New')
            return super(MaintenanceTicket, self).create(vals)

    def action_new(self):
        self.state = 'new'

    def action_approved(self):
        self.state = 'approved'


    def action_assigned(self):
        self.state = 'assigned'
        self.assigned_date = fields.Datetime.now()

    def action_in_progress(self):
        self.state = 'in_progress'
        self.date_in_progress = fields.Datetime.now()

    def action_resolved(self):
        self.state = 'resolved'
        self.date_resolved = fields.Datetime.now()

    def action_closed(self):
        self.state = 'closed'
        self.close_date = fields.Datetime.now()

    def action_cancelled(self):
        self.state = 'cancelled'

#     Email to notify Maintenance Team Member of Maintenance Ticket Assigned to them

    def send_assigned_task_notification_email_template(self):
        model_id = self.env['maintenance.ticket']
        form = self.env.ref('ea_equipment_tracking.maintenance_ticket_form.')
        action_id = self.env.ref('ea_equipment_tracking.maintenance_tickets_menu_action')
        self.url = '/web#id=' + str(self.id) + '&view_type=form&model=ea_equipment_tracking&action=' + str(action_id.id)

        rendering_context = dict(self._context)
        rendering_context.update({
            'action_id': self.env.ref('ea_equipment_tracking.maintenance_tickets_menu_action').id,
            'dbname': self._cr.dbname,
            'base_url': self.env['ir.config_parameter'].get_param('web.base.url', default='http://localhost:8069')
        })

        template = self.env.ref('ea_equipment_tracking.assigned_ticket_email_template')
        self.env['mail.template'].browse(template.id).with_context(rendering_context).send_mail(self.id, force_send=True)

        return True








































