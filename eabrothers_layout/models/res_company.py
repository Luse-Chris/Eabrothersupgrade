# -*- coding: utf-8 -*-
from odoo import models,fields

class Company(models.Model):
    _inherit = "res.company"
    document_header = fields.Binary(string="Document Header")
    document_footer = fields.Binary(string="Document Footer")

class BaseDocumentLayout(models.TransientModel):
    """
    Inherit BaseDocumentLayout to add Company fields
    that Odoo don't have taken into account
    """
    _inherit = 'base.document.layout'
    # Those following fields are required as a company to create invoice report
    document_header = fields.Binary(related='company_id.document_header', readonly=True)
    document_footer = fields.Binary(related='company_id.document_footer', readonly=True)
