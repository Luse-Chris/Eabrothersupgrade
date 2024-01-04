# -*- coding: utf-8 -*-
from odoo import models,fields

class Company(models.Model):
    _inherit = "res.company"
    document_header = fields.Binary(string="Document Header")
    document_footer = fields.Binary(string="Document Footer")

