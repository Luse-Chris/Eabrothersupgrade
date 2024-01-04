# -*- coding: utf-8 -*-

from odoo import models, fields



class CustomerTicketsListWizard(models.TransientModel):
    _name = 'customer_tickets_list.wizard'
    _description = 'Customer Tickets List Wizard'

    equipment_owner_id = fields.Many2one('equipment.owner', required=True, string='Equipment Owner')
    date_from = fields.Date(default=fields.Date.today, required=True, string='Start Date')
    date_to = fields.Date(default=fields.Date.today, required=True, string='End Date')

    def generate_excel_report(self):
        data = {'form': self.read(['equipment_owner_id', 'date_from', 'date_to'])[0]}
        return self._print_report(data)

    def _print_report(self, data):
        return self.env.ref('ea_equipment_tracking.customer_tickets_list_excel_report').report_action(self, data=data)

      
