# -*- coding: utf-8 -*-
# from odoo import http


# class EabrothersLayout(http.Controller):
#     @http.route('/eabrothers_layout/eabrothers_layout/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eabrothers_layout/eabrothers_layout/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('eabrothers_layout.listing', {
#             'root': '/eabrothers_layout/eabrothers_layout',
#             'objects': http.request.env['eabrothers_layout.eabrothers_layout'].search([]),
#         })

#     @http.route('/eabrothers_layout/eabrothers_layout/objects/<model("eabrothers_layout.eabrothers_layout"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eabrothers_layout.object', {
#             'object': obj
#         })
