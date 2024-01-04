# -*- coding: utf-8 -*-

from odoo import fields, models


class BranchEquipmentListXlsxReportWizard(models.TransientModel):
    _name = 'branch_equipment_list_xlsx_report.wizard'

    equipment_owner_id = fields.Many2one('equipment.owner', required=True, string='Equipment Owner')
    location_id = fields.Many2one('customer.location', required=True, string='Equipment Location')

    def generate_excel_report(self):
        data = {'form': self.read(['equipment_owner_id', 'location_id'])[0]}
        return self._print_report(data)

    def _print_report(self, data):
        return self.env.ref('ea_equipment_tracking.branch_equipment_list_excel_report').report_action(self, data=data)

