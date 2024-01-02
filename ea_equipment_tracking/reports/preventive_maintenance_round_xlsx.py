# -*- coding: utf-8 -*-

from odoo import models, fields



class PreventiveMaintenanceRoundXlsx(models.AbstractModel):
    _name = 'report.ea_equipment_tracking.report_preventive_maintenance'
    _inherit = 'report.odoo_report_xlsx.abstract' 
    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet("Preventive Maintenance Round")
#         Formats
        format_header_right = workbook.add_format({'bg_color': '#d3ffce', 'bold': True, 'align': 'right'})
        format_header_left = workbook.add_format({'bg_color': '#d3ffce', 'bold': True, 'align': 'left'})
        format_bold_align_left = workbook.add_format({'bold': True})
        format_table_header = workbook.add_format({'bold': True, 'bg_color': '#d3ffce', 'border': True, 'align': 'center'})
        format_normal_text = workbook.add_format({'border': True})
        format_normal_text_merged = workbook.add_format({'border': True, 'align': 'left', 'valign': 'top', 'text_wrap': True})
        format_ticket_break = workbook.add_format({'bg_color': '#d3ffce', 'border': True})

#         Setting Column Widths
        sheet.set_column('A:A', 3)
        sheet.set_column('B:B', 19.5)
        sheet.set_column('C:C', 17)
        sheet.set_column('D:D', 25)
        sheet.set_column('E:E', 14)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 16.4)
        sheet.set_column('H:H', 20)
        sheet.set_column('I:I', 20)

#         Report Template
        sheet.merge_range('B2:E2', 'Preventive Maintenance Report -', format_header_right)
        sheet.merge_range('F2:I2', data["pm_round"]["name"], format_header_left)
        sheet.write('B4', 'Equipment Owner:', format_bold_align_left)
        sheet.merge_range('C4:D4', data["form"]["equipment_owner_id"][1])
        sheet.write('B5', 'Location:', format_bold_align_left)
        sheet.merge_range('C5:D5', data["pm_round"]["name"])
        sheet.write('B6', 'Equipment Category:', format_bold_align_left)
        sheet.merge_range('C6:D6', data["form"]["equipment_category_id"][1])
        sheet.write('H4', 'Start Date', format_bold_align_left)
        sheet.write('I4', data["pm_round"]["commenced_on"])
        sheet.write('H6', 'End Date', format_bold_align_left)
        sheet.write('I6', data["pm_round"]["date_ended"])

        sheet.merge_range('B8:C8', 'Equipment Details', format_table_header)
        sheet.write('D8', 'Place Installed', format_table_header)
        sheet.write('E8', 'Date of Service', format_table_header)
        sheet.write('F8', 'Service Done', format_table_header)
        sheet.write('G8', 'Reference', format_table_header)
        sheet.write('H8', 'Equipment Status', format_table_header)
        sheet.write('I8', 'Remarks', format_table_header)

        row = 8
        lines = self.env['pm.lines'].search([('equipment_owner_id', '=', data["form"]["equipment_owner_id"][0]),
                                             ('equipment_lines', '=', data["form"]["pm_round_id"][0])

                                                     ])
        for pm_item in lines:
            sheet.write(row, 1, 'Make:', format_normal_text)
            sheet.write(row, 2, pm_item.equipment_id.make, format_normal_text)
            sheet.write(row+1, 1, 'Model:', format_normal_text)
            sheet.write(row+1, 2, pm_item.equipment_id.model, format_normal_text)
            sheet.write(row+2, 1, 'Serial #:', format_normal_text)
            sheet.write(row+2, 2, pm_item.equipment_id.name, format_normal_text)
            sheet.write(row+3, 1, 'Capacity', format_normal_text)
            sheet.write(row+3, 2, pm_item.equipment_id.capacity, format_normal_text)
            sheet.merge_range(row, 3, row+3, 3, pm_item.where_installed.name, format_normal_text_merged)
            sheet.merge_range(row, 4, row+3, 4, fields.Date.to_string(pm_item.service_date), format_normal_text_merged)
            sheet.merge_range(row, 5, row+3, 5, pm_item.service_done, format_normal_text_merged)
            sheet.merge_range(row, 6, row + 3, 6, pm_item.reference, format_normal_text_merged)
            sheet.merge_range(row, 7, row+3, 7, pm_item.equipment_status, format_normal_text_merged)
            sheet.merge_range(row, 8, row+3, 8, pm_item.remarks, format_normal_text_merged)
            sheet.merge_range(row+4, 1, row+4, 8, '', format_ticket_break)

            row += 5
