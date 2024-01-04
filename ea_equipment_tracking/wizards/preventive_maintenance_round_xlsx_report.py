# -*- coding: utf-8 -*-

from odoo import fields, models

class PreventiveMaintenanceRoundXlsxReportWizard(models.TransientModel):
    _name = 'preventive_maintenance_round_xlsx_report.wizard'
    _description = 'PM Round Xlsx Report Wizard'

    equipment_owner_id = fields.Many2one('equipment.owner', required=True, string='Equipment Owner')
    pm_round_id = fields.Many2one('preventive.maintenance', required=True, string='PM Round Title')
    equipment_category_id = fields.Many2one('equipment.category', required=True, string='Equipment Category')

    def generate_excel_report(self):
        data = {'form': self.read(['equipment_owner_id', 'pm_round_id', 'equipment_category_id'])[0]}
        pm_round = self.env["preventive.maintenance"].browse(data["form"]["pm_round_id"][0])

        data["pm_round"] = {
            "name": pm_round.name,
            "location": pm_round.location_id.name,
            "commenced_on": pm_round.commenced_on,
            "date_ended": pm_round.date_ended
        }

        return self._print_report(data)

    def _print_report(self, data):
        return self.env.ref('ea_equipment_tracking.preventive_maintenance_round_excel_report').report_action(self,
                                                                                                             data=data)
