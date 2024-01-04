# -*- coding: utf-8 -*-

from odoo import fields, models


class TeamTicketsWizard(models.TransientModel):
    _name = 'team_tickets.wizard'
    _description = 'Team Tickets Report Wizard'

    responsible_team_id = fields.Many2one('maintenance.team', required=True, string='Maintenance Team')
    date_from = fields.Date(default=fields.Date.today, required=True, string='Start Date')
    date_to = fields.Date(default=fields.Date.today, required=True, string='End Date')

    def fetch_report(self):
        data = {'form': self.read(['responsible_team_id', 'date_from', 'date_to'])[0]}
        return self._print_report(data)

    def print_report(self):
        self.ensure_one()
        [data] = self.read()
        datas = {
            'model': 'maintenance.team',
            'form': data,
        }
        return self.env.ref('ea_equipment_tracking.tickets_team_wise_report').report_action(self, data=datas)





# class ReportTeamTickets(models.AbstractModel):
#     _name = 'report.ea_equipment_tracking.report_team_tickets'

#     @api.model
#     def render_html(self, docids, data=None):
#         self.model = self.env.context.get('active_model')
#         docs = self.env[self.model].browse(self.env.context.get('active_id'))
#         ticket_records = []
#         tickets = self.env['maintenance.ticket'].search([('responsible_team_id', '=', docs.responsible_team_id.id),
#                                                          ('state', '!=', ('new', 'approved', 'cancelled'))])
#         if docs.date_from and docs.date_to:
#             for ticket in tickets:
#                 if parse(docs.date_from) <= parse(ticket.assigned_date) and parse(docs.date_to) >= parse(ticket.assigned_date):
#                     ticket_records.append(ticket);

#             docargs = {
#                 'doc_ids': self.ids,
#                 'doc_model': self.model,
#                 'docs': docs,
#                 'time': time,
#                 'tickets': ticket_records
#             }
#             return self.env['report'].render('ea_equipment_tracking.report_team_tickets', docargs)
