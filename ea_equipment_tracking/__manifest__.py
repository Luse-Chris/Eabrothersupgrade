# -*- coding: utf-8 -*-
{
    'name': "ea_equipment_tracking",


    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'hr', 'mail','odoo_report_xlsx',],

    # always loaded
    'data': [
        'security/equipment_tracking_security.xml',
        'security/ir.model.access.csv',
        'views/notify_assigned_task_template.xml',
        'views/maintenance_ticket.xml',
        # 'views/ticket_workflow.xml',
        'views/sale_order_line.xml',
        'views/sequence.xml',
        'views/equipment.xml',
        'views/configuration.xml',
        'views/preventive_maintenance.xml',
        'wizards/branch_equipment_list_xlsx_report.xml',

        'wizards/customer_tickets_report.xml',
        'reports/customer_tickets.xml',
        'wizards/customer_tickets_list.xml',
        'wizards/equipment_tickets_report.xml',
        'reports/equipment_tickets.xml',
        'wizards/team_tickets_report.xml',
        'reports/team_tickets.xml',
        # 'reports/ticket_summary.xml',
        # 'reports/owner_equipment_summary.xml',
        'wizards/equipment_cost_report.xml',
        'reports/equipment_cost.xml',
        'reports/customer_tickets_list_xlsx.xml',
        'wizards/equipment_technical_xlsx_report.xml',
        'reports/technical_report_xlsx.xml',
        'reports/preventive_maintenance_round_xlsx.xml',
        'wizards/preventive_maintenance_round_xlsx_report.xml',
        'reports/branch_equipment_list_xlsx.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
