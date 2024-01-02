from odoo import models
from datetime import datetime


class CustomerTicketsList(models.AbstractModel):
    _name = 'report.ea_equipment_tracking.report_customer_tickets_list'
    _inherit = 'report.odoo_report_xlsx.abstract'    
    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet("Maintenance Tickets List")
        form = data.get("form")
        date_from = form["date_from"]
        date_to = form["date_to"]
        equipment_owner = form["equipment_owner_id"]
#         Formats
        format_grey_bg_bold = workbook.add_format({'font_size': 11, 'bg_color': '#d3ffce', 'bold': True, 'align': 'center'})
        format_grey_bg = workbook.add_format({'font_size': 11, 'bg_color': '#d3ffce', 'align': 'center'})
        format_bold = workbook.add_format({'font_size': 11, 'bold': True, 'align': 'center'})
        format_normal_text = workbook.add_format({'font_size': 11, 'align': 'left'})
        format_date = workbook.add_format({'num_format': 'dd/mm/yyyy', 'font_size': 11, 'align': 'left'})

#         Setting Column Widths
        sheet.set_column('A:A', 5)
        sheet.set_column('B:S', 18)


#         Report Template
        sheet.merge_range('A1:S1', 'Maintenance Ticket Details', format_grey_bg_bold)
        sheet.merge_range('A3:B3', 'Equipment Owner', format_bold)
        sheet.merge_range('C3:E3', equipment_owner[1], format_grey_bg)
        sheet.write('G3', 'Date From', format_bold)
        sheet.write('H3', date_from, format_grey_bg)
        sheet.write('J3', 'Date To', format_bold)
        sheet.write('K3', date_to, format_grey_bg)
        sheet.write('A5', 'S/n', format_grey_bg_bold)
        sheet.write('B5', 'Ticket Number', format_grey_bg_bold)
        sheet.write('C5', 'Subject', format_grey_bg_bold)
        sheet.write('D5', 'Customer Reference', format_grey_bg_bold)
        sheet.write('E5', 'Reported By', format_grey_bg_bold)
        sheet.write('F5', 'Phone/Email', format_grey_bg_bold)
        sheet.write('G5', 'Affected Equipment', format_grey_bg_bold)
        sheet.write('H5', 'Alternative ID #', format_grey_bg_bold)
        sheet.write('I5', 'Category', format_grey_bg_bold)
        sheet.write('J5', 'Location', format_grey_bg_bold)
        sheet.write('K5', 'Place', format_grey_bg_bold)
        sheet.write('L5', 'Date Reported', format_grey_bg_bold)
        sheet.write('M5', 'Responsible Team', format_grey_bg_bold)
        sheet.write('N5', 'Assigned To', format_grey_bg_bold)
        sheet.write('O5', 'Assigned Date', format_grey_bg_bold)
        sheet.write('P5', 'Scheduled Date', format_grey_bg_bold)
        sheet.write('Q5', 'Date Closed', format_grey_bg_bold)
        sheet.write('R5', 'Problem Description', format_grey_bg_bold)
        sheet.write('S5', 'Problem Resolution', format_grey_bg_bold)

        ticket_records = []
        row = 5
        tickets = self.env['maintenance.ticket'].search([('equipment_owner_id', '=', equipment_owner[0]),
                                                         ('reporting_date', '>=', date_from),
                                                         ('reporting_date', '<=', date_to)])
        for ticket in tickets:
            sheet.write(row, 1, ticket.name, format_normal_text)
            sheet.write(row, 2, ticket.subject, format_normal_text)

            if ticket.customer_ref:
                sheet.write(row, 3, ticket.customer_ref, format_normal_text)
            else:
                sheet.write(row, 3, '-', format_normal_text)

            sheet.write(row, 4, ticket.reported_by_name, format_normal_text)

            if ticket.reported_by_phone:
                sheet.write(row, 5, ticket.reported_by_phone, format_normal_text)
            else:
                sheet.write(row, 5, '-', format_normal_text)

            if ticket.equipment_id:
                sheet.write(row, 6, ticket.equipment_id.name, format_normal_text)
            else:
                sheet.write(row, 6, '-', format_normal_text)

            if ticket.tag_id_number:
                sheet.write(row, 7, ticket.tag_id_number, format_normal_text)
            else:
                sheet.write(row, 7, '-', format_normal_text)

            if ticket.category_id.name:
                sheet.write(row, 8, ticket.category_id.name, format_normal_text)
            else:
                sheet.write(row, 8, '-', format_normal_text)

            if ticket.location:
                sheet.write(row, 9, ticket.location.name, format_normal_text)
            else:
                sheet.write(row, 9, '-', format_normal_text)

            if ticket.where_installed:
                sheet.write(row, 10, ticket.where_installed.name, format_normal_text)
            else:
                sheet.write(row, 10, '-', format_normal_text)

            sheet.write(row, 11, ticket.reporting_date, format_date)

            if ticket.responsible_team_id:
                sheet.write(row, 12, ticket.responsible_team_id.name, format_normal_text)
            else:
                sheet.write(row, 12, '-', format_normal_text)

            if ticket.assigned_to_id:
                sheet.write(row, 13, ticket.assigned_to_id.name, format_normal_text)
            else:
                sheet.write(row, 13, '-', format_normal_text)

            if ticket.assigned_date:
                sheet.write(row, 14, ticket.assigned_date, format_date)
            else:
                sheet.write(row, 14, '-', format_date)

            if ticket.scheduled_date:
                sheet.write(row, 15, ticket.scheduled_date, format_date)
            else:
                sheet.write(row, 15, '-', format_date)

            if ticket.close_date:
                sheet.write(row, 16, ticket.close_date, format_date)
            else:
                sheet.write(row, 16, '-', format_date)

            if ticket.description:
                sheet.write(row, 17, ticket.description, format_normal_text)
            else:
                sheet.write(row, 17, '-', format_normal_text)

            if ticket.resolution:
                sheet.write(row, 18, ticket.resolution, format_normal_text)
            else:
                sheet.write(row, 18, '-', format_normal_text)
            row += 1
