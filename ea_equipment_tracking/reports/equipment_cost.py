# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import UserError
from pprint import  pprint
import time


class EquipmentCostReport(models.AbstractModel):
    _name = 'report.ea_equipment_tracking.report_equipment_cost'
    _description = 'Equipment cost report'

    def _get_header_info(self, form):
        equipment = self.env["equipment"].browse(form["equipment_id"][0])
        return {
            'date_from': form["date_from"],
            'date_to': form["date_to"],
            'equipment_name': equipment.name,
            "equipment_location": equipment.location.name,
            "equipment_category": equipment.category_id.name, 
            "equipment_owner": equipment.equipment_owner_id.name,
            "order_line_total": equipment.order_line_total,

        }
    @api.model
    def _get_report_values(self, docids, data=None):
        form = data.get("form")
        if not form:
            raise UserError(
                _("Form content is missing, this report cannot be printed."))
        pprint(form)
        costs = self.env['sale.order.line'].search(
            [('equipment_id', '=', form["equipment_id"][0]), ('order_confirmation_date', '>=', form["date_from"]), ('order_confirmation_date', '<=', form["date_to"]), ('state', '=', 'sale')])
        return {
            'doc_ids': data.get("ids"),
            'doc_model': data.get("model"),
            'get_header_info': self._get_header_info(data["form"]),
            'time': time,
            'costs': costs
        }

