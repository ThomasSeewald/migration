# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################
from odoo import models, fields, api, _

class gelbeseiten_gelbeseiten(models.Model):
	_name = 'gelbeseiten.gelbeseiten'
	_description = 'Adressen der potentiellen Arbeitgeber'

	name = fields.Char(string='Name', required=1)



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: