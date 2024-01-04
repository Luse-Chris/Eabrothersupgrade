# -*- coding: utf-8 -*-

from odoo import fields, models


class EquipmentCostWizard(models.TransientModel):
    _name = 'equipment_cost.wizard'
    _description = 'Equipment Cost Wizard'

    equipment_id = fields.Many2one('equipment', required=True, string='Equipment Serial #')
    date_from = fields.Date(default=fields.Date.today, required=True, string='Start Date')
    date_to = fields.Date(default=fields.Date.today, required=True, string='End Date')

    def fetch_report(self):
        data = {'form': self.read(['equipment_id', 'date_from', 'date_to'])[0]}
        # return self.env['report'].get_action(self, 'ea_equipment_tracking.report_equipment_cost', data=data)
        return self.env.ref('ea_equipment_tracking.report_equipment_cost').report_action(self, data=data)

        # report_equipment_cost is the name of our report template
    def print_report(self):
        self.ensure_one()
        [data] = self.read()
        # print(data)
        equipment = self.env['equipment'].browse(data['equipment_id'])
        # print({"equipment_id": equipment_id})
        # data["equipment"] = self.env['sale.order.line'].browse(data.get("equipment_id")[0])
        datas = {
            'ids': [],
            'model': 'sale.order.line',
            'form': data,
            "docs": self
        }
        return self.env.ref('ea_equipment_tracking.equipment_cost_report').report_action(self, data=datas)



# class ReportEquipmentCost(models.AbstractModel):
#     _name = 'report.ea_equipment_tracking.report_equipment_cost'
#     @api.model
#     def render_html(self, docids, data=None):
#         print("Rendering ....")
#         self.model = self.env.context.get('active_model')
#         docs = self.env[self.model].browse(self.env.context.get('active_id'))
#         cost_records = []
#         costs = self.env['sale.order.line'].search(
#             [('equipment_id', '=', docs.equipment_id.id), ('order_confirmation_date', '=>')])
#         if docs.date_from and docs.date_to:
#             for cost in costs:
#                 if parse(docs.date_from) <= parse(cost.order_confirmation_date) and parse(docs.date_to) >= parse(cost.order_confirmation_date):
#                     cost_records.append(cost);

#             docargs = {
#                 'doc_ids': self.ids,
#                 'doc_model': self.model,
#                 'docs': docs,
#                 'time': time,
#                 'costs': cost_records
#             }
#             return self.env['report'].render('ea_equipment_tracking.report_equipment_cost', docargs)

