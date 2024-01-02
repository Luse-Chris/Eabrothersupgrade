# -*- coding: utf-8 -*-

from odoo import fields, models



class EquipmentTicketsWizard(models.TransientModel):
    _name = 'equipment_tickets.wizard'
    _description = 'Equipment Tickets Report Wizard'

    equipment_id = fields.Many2one('equipment', required=True, string='Equipment')
    date_from = fields.Date(default=fields.Date.today, required=True, string='Start Date')
    date_to = fields.Date(default=fields.Date.today, required=True, string='End Date')

    def fetch_report(self):
        data = {'form': self.read(['equipment_id', 'date_from', 'date_to'])[0]}
        return self._print_report(data)

    def print_report(self):
        self.ensure_one()
        [data] = self.read()
        datas = {
            'model': 'maintenance.ticket',
            'form': data,
        }
        return self.env.ref('ea_equipment_tracking.tickets_equipment_wise_report').report_action(self, data=datas)


