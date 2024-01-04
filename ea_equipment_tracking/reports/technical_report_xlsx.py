from odoo import models, fields



class TechnicalReportXls(models.AbstractModel):
    _name = 'report.ea_equipment_tracking.report_equipment_technical_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet('Technical Report')
        date_from = data["form"]["date_from"]
        date_to = data["form"]["date_to"]
        equipment_owner = data["form"]["equipment_owner_id"]
        equipment_category = data["form"]["equipment_category_id"]

        # Formats
        format_grey_bg_bold = workbook.add_format({'bg_color': '#d3ffce', 'bold': True, 'align': 'center', 'border': True})
        format_ticket_break = workbook.add_format({'bg_color': '#d3ffce', 'border': True})
        format_ticket_merged_cells = workbook.add_format({'align': 'left', 'valign': 'top', 'text_wrap': True, 'border': True})
        format_normal_text = workbook.add_format({'border': True})
        format_grey_bg_bold_right = workbook.add_format({'bg_color': '#d3ffce', 'bold': True, 'align': 'right'})
        format_grey_bg_bold_left = workbook.add_format({'bg_color': '#d3ffce', 'bold': True, 'align': 'left'})
        format_grey_bg = workbook.add_format({'bg_color': '#d3ffce', 'align': 'center'})
        format_bold = workbook.add_format({'bold': True, 'align': 'right'})

        # Setting Column Width
        sheet.set_column('A:A', 3)
        sheet.set_column('B:B', 11)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 15)
        sheet.set_column('E:E', 19)
        sheet.set_column('F:H', 20)

        # Report Template
        sheet.merge_range('A2:E2', 'Technical Report -', format_grey_bg_bold_right)
        sheet.merge_range('F2:H2', equipment_category[1], format_grey_bg_bold_left)
        sheet.write('B4', 'Customer:', format_bold)
        sheet.write('C4', equipment_owner[1], format_grey_bg)
        sheet.write('D4', 'Start Date:', format_bold)
        sheet.write('E4', date_from, format_grey_bg)
        sheet.write('F4', 'End Date:', format_bold)
        sheet.write('G4',  date_to, format_grey_bg)

        sheet.merge_range('B6:C6', 'Equipment Details', format_grey_bg_bold)
        sheet.write('D6', 'Branch', format_grey_bg_bold)
        sheet.write('E6', 'Attended By', format_grey_bg_bold)
        sheet.write('F6', 'Problem Description', format_grey_bg_bold)
        sheet.write('G6', 'Detailed Resolution', format_grey_bg_bold)
        sheet.write('H6', 'Remarks', format_grey_bg_bold)

        row = 6
        tickets = self.env['maintenance.ticket'].search([('equipment_owner_id', '=', equipment_owner[0]),
                                                         ('category_id', '=', equipment_category[0]),
                                                         ('reporting_date', '>=', date_from),
                                                         ('reporting_date', '<=', date_to),
                                                         ])
        for ticket in tickets:
            sheet.write(row, 1, 'Ticket #:', format_normal_text)
            sheet.write(row+1, 1, 'Customer Ref:', format_normal_text)
            sheet.write(row+2, 1, 'Location:', format_normal_text)
            sheet.write(row+3, 1, 'Serial #:', format_normal_text)
            sheet.write(row+4, 1, 'Model:', format_normal_text)
            sheet.write(row+5, 1, 'Tag ID:', format_normal_text)
            sheet.write(row+6, 1, 'Date Opened:', format_normal_text)
            sheet.write(row+7, 1, 'Date Closed:', format_normal_text)
            sheet.merge_range(row+8, 1, row+8, 7, '', format_ticket_break)
            sheet.write(row, 2, ticket.name, format_normal_text)
            sheet.write(row+1, 2, ticket.customer_ref or "-", format_normal_text)
            sheet.write(row+2, 2, ticket.where_installed.name or "-", format_normal_text)
            sheet.write(row+3, 2, ticket.serial_number or "-", format_normal_text)
            sheet.write(row+4, 2, ticket.equipment_id.model or "-", format_normal_text)
            sheet.write(row+5, 2, ticket.tag_id_number or "-", format_normal_text)
            sheet.write(row+6, 2, fields.Date.to_string(ticket.reporting_date), format_normal_text)
            sheet.write(row+7, 2, fields.Date.to_string(ticket.close_date) if ticket.close_date else "-", format_normal_text)
            sheet.merge_range(row, 3, row+7, 3, ticket.location.name or "-", format_ticket_merged_cells)
            sheet.merge_range(row, 4, row+7, 4, ticket.assigned_to_id.name or "[Unassigned]", format_ticket_merged_cells)
            sheet.merge_range(row, 5, row+7, 5, ticket.description or "-", format_ticket_merged_cells)
            sheet.merge_range(row, 6, row+7, 6, ticket.resolution or "-", format_ticket_merged_cells)
            sheet.merge_range(row, 7, row+7, 7, ticket.remarks or "-", format_ticket_merged_cells)
            row += 9
