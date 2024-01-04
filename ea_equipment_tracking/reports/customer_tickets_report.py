
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CustomerTicketsReport(models.AbstractModel):
    _name = 'report.ea_equipment_tracking.report_customer_tickets'
    _description = 'Customer-wise Report'

    def _get_header_info(self, form):
        return {
            'date_from': form["date_from"],
            'date_to': form["date_to"],
            'equipment_owner': form["equipment_owner_id"][1]

        }

    @api.model
    def _get_report_values(self, docids, data=None):
        form = data.get("form")
        if not form:
            raise UserError(
                _("Form content is missing, this report cannot be printed."))
        tickets = self.env['maintenance.ticket'].search([('equipment_owner_id', '=', data["form"]["equipment_owner_id"][0]),
                                                         ('state', '=', 'closed'), ('close_date', '>=', form["date_from"]), ('close_date', '<=', form["date_to"])])
        docargs = {
            'get_header_info': self._get_header_info(data["form"]),
            'tickets': tickets
        }
        return docargs
