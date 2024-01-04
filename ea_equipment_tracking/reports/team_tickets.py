
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class TeamTicketsReport(models.AbstractModel):
    _name = 'report.ea_equipment_tracking.report_team_tickets'
    _description = 'Team-wise Report'

    def _get_header_info(self, form):
        return {
            'date_from': form["date_from"],
            'date_to': form["date_to"],
            'responsible_team': form["responsible_team_id"][1]

        }

    @api.model
    def _get_report_values(self, docids, data=None):
        form = data.get("form")
        if not form:
            raise UserError(
                _("Form content is missing, this report cannot be printed."))
        tickets = self.env['maintenance.ticket'].search([('responsible_team_id', '=', form['responsible_team_id'][0]),
                                                         ('state', '!=', ('new', 'approved', 'cancelled')), ('assigned_date', '>=', form["date_from"]), ('assigned_date', '<=', form["date_to"])])
        return {
            'get_header_info': self._get_header_info(data["form"]),
            'tickets': tickets
        }

