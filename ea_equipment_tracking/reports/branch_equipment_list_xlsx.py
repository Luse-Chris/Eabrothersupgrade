# -*- coding: utf-8 -*-

from odoo import models
from datetime import datetime


class BranchEquipmentListXls(models.AbstractModel):
    _name = 'report.ea_equipment_tracking.report_branch_equipment_list'
    _inherit = 'report.report_xlsx.abstract'
    def generate_xlsx_report(self, workbook, data, lines):
        form = data.get("form")
        equipment_owner = form["equipment_owner_id"]
        location = form["location_id"]

        sheet = workbook.add_worksheet('Equipment List')

#         Formats
        format_bold = workbook.add_format({'bold': True, 'align': 'center'})
        format_bg_color = workbook.add_format(
            {'bg_color': '#d3ffce', 'align': 'left'})

#       Setting Column Widths
        sheet.set_column('A:A', 3)
        sheet.set_column('B:B', 11)
        sheet.set_column('C:G', 15)
        sheet.set_column('H:H', 19)

#         Report layout
        sheet.merge_range(
            'B1:H1', 'List of Active Equipment per Category', format_bold)
        sheet.write('B3', 'Location', format_bold)
        sheet.merge_range('C3:D3', location[1], format_bg_color)

        row = 5
        sheet.write(row, 1, 'Category', format_bold)
        sheet.write(row, 2, 'Primary ID', format_bold)
        sheet.write(row, 3, 'Alternative ID', format_bold)
        sheet.write(row, 4, 'Make', format_bold)
        sheet.write(row, 5, 'Model', format_bold)
        sheet.write(row, 6, 'Capacity', format_bold)
        sheet.write(row, 7, 'Where Installed', format_bold)

        row = 6

        equipment_category = []
        categories = self.env['equipment.category'].search([])
        for category in categories:
            equipment_category.append(category.id)
            equipments_list = []
            equipment = self.env['equipment'].search([('equipment_owner_id', '=', equipment_owner[0]),
                                                      ('location', '=',
                                                       location[0]),
                                                      ('category_id',
                                                       '=', category.id),
                                                      ('active', '=', True)])

            sheet.merge_range(row, 1, row, 7, category.name, format_bg_color)

            for equipment in equipment:
                row += 1
                equipments_list.append(equipment.id)
                if equipments_list:
                    sheet.write(row, 2, equipment.name)
                    sheet.write(row, 3, equipment.tag_id_number or "-")
                    sheet.write(row, 4, equipment.make or "-")
                    sheet.write(row, 5, equipment.model or "-")
                    sheet.write(row, 6, equipment.capacity or "-")
                    sheet.write(row, 7, equipment.where_installed.name or "-")
            row += 1

            if not equipments_list:
                sheet.merge_range(row + 1, 2, row + 1, 7,
                                  "[No Equipment For This Category]")
                row += 2

        
