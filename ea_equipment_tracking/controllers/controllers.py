# -*- coding: utf-8 -*-
# from odoo import http


# class EaEquipmentTracking(http.Controller):
#     @http.route('/ea_equipment_tracking/ea_equipment_tracking/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ea_equipment_tracking/ea_equipment_tracking/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ea_equipment_tracking.listing', {
#             'root': '/ea_equipment_tracking/ea_equipment_tracking',
#             'objects': http.request.env['ea_equipment_tracking.ea_equipment_tracking'].search([]),
#         })

#     @http.route('/ea_equipment_tracking/ea_equipment_tracking/objects/<model("ea_equipment_tracking.ea_equipment_tracking"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ea_equipment_tracking.object', {
#             'object': obj
#         })
