# -*- coding: utf-8 -*-
import base64
import io
import logging
import os
import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError
from odoo.modules.module import get_resource_path

from random import randrange
from PIL import Image

_logger = logging.getLogger(__name__)


class Company(models.Model):
    _inherit = "res.company"

    def _get_header_image(self):
        return base64.b64encode(open(os.path.join(tools.config['root_path'], 'addons', 'base', 'static', 'img',
                                                  'res_company_document_header_png.png'), 'rb').read())

    # def _get_footer_image(self):
    #     return base64.b64encode(open(os.path.join(tools.config['root_path'], 'addons', 'base', 'static', 'img', 'res_company_document_footer_png.png'), 'rb') .read())

    document_header_png = fields.Binary(related='partner_id.image_1920', default=_get_header_image,
                                        string="Company Header Image", readonly=False)

    # document_footer_png = fields.Binary(default=_get_footer_image, string="Company Footer Image", readonly=False)
