# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EquipmentTicketsReport(models.AbstractModel):
    _name = 'report.ea_equipment_tracking.report_equipment_tickets'
    _description = 'Equipment cost report'

    def _get_header_info(self, form):
        equipment = self.env["equipment"].browse(form["equipment_id"][0])
        return {
            'date_from': form["date_from"],
            'date_to': form["date_to"],
            'equipment_id': equipment.id,
            "equipment_category": equipment.category_id.name,
            "equipment_owner": equipment.equipment_owner_id.name,
        }

    @api.model
    def _get_report_values(self, docids, data=None):
        form = data.get("form")
        if not form:
            raise UserError(
                _("Form content is missing, this report cannot be printed."))
        tickets = self.env['maintenance.ticket'].search(
            [('equipment_id', '=', form["equipment_id"][0])])
        return {
            # 'doc_model': self.model,
            'get_header_info': self._get_header_info(data["form"]),
            'tickets': tickets
        }

