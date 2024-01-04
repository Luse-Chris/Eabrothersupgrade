# -*- coding: utf-8 -*-

from odoo import fields, models


class EquipmentTechnicalXlsxReportWizard(models.TransientModel):
    _name = 'equipment_technical_xlsx_report.wizard'
    _description = 'Equipment Technical Xlsx Report Wizard'

    equipment_owner_id = fields.Many2one('equipment.owner', required=True, string='Equipment Owner')
    equipment_category_id = fields.Many2one('equipment.category', required=True, string='Equipment Category')
    date_from = fields.Date(default=fields.Date.today, required=True, string='Start Date')
    date_to = fields.Date(default=fields.Date.today, required=True, string='End Date')
    
    def generate_excel_report(self):
        data = {'form': self.read(['equipment_owner_id', 'date_from', 'date_to', 'equipment_category_id'])[0]}
        return self._print_report(data)

    def _print_report(self, data):
        return self.env.ref('ea_equipment_tracking.equipment_technical_report_excel_report').report_action(self, data=data)
        # report_equipment_technical_xlsx is name of our report template
