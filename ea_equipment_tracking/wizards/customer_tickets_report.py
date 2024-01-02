# -*- coding: utf-8 -*-

from odoo import models, fields


class CustomerTicketsWizard(models.TransientModel):
    _name = 'customer_tickets.wizard'
    _description = 'Customer Tickets Report Wizard'

    equipment_owner_id = fields.Many2one('equipment.owner', required=True, string='Equipment Owner')
    date_from = fields.Date(default=fields.Date.today, required=True, string='Start Date')
    date_to = fields.Date(default=fields.Date.today, required=True, string='End Date')

    def print_report(self):
        self.ensure_one()
        [data] = self.read()
        datas = {
            'form': data,
        }
        return self.env.ref('ea_equipment_tracking.closed_customer_tickets_report').report_action(self, data=datas)


# class ReportCustomerTickets(models.AbstractModel):
#     _name = 'report.ea_equipment_tracking.report_customer_tickets'

#     @api.model
#     def render_html(self, docids, data=None):
#         self.model = self.env.context.get('active_model')
#         docs = self.env[self.model].browse(self.env.context.get('active_id'))
#         ticket_records = []
#         tickets = self.env['maintenance.ticket'].search([('equipment_owner_id', '=', docs.equipment_owner_id.id),
#                                                          ('state', '=', 'closed')])
#         if docs.date_from and docs.date_to:
#             for ticket in tickets:
#                 if parse(docs.date_from) <= parse(ticket.close_date) and parse(docs.date_to) >= parse(ticket.close_date):
#                     ticket_records.append(ticket);

#             docargs = {
#                 'doc_ids': self.ids,
#                 'doc_model': self.model,
#                 'docs': docs,
#                 'time': time,
#                 'tickets': ticket_records
#             }
#             return self.env['report'].render('ea_equipment_tracking.report_customer_tickets', docargs)
