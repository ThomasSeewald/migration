# -*- coding: utf-8 -*-

from lxml import etree

from odoo import fields, models
from odoo.exceptions import ValidationError


class IrModelImportWizard(models.TransientModel):
    _inherit = 'ir.model.import.wizard'

    menu_name = fields.Char('Menu Name')
    parent_menu_id = fields.Many2one("ir.ui.menu", string="Parent Menu")

    def add_fields_in_views(self, sheet, model, new_fields):
        try:
            super().add_fields_in_views(sheet, model, new_fields)
        except ValidationError:
            xml_tree = etree.Element("tree")
            index = 0
            for field in new_fields:
                field = etree.SubElement(xml_tree, "field", name=field.name)
                index += 1
                if index == 4:
                    break

            IrView = self.env['ir.ui.view']
            IrView.create({
                'name': '%s.tree.view' % (model.model),
                'type': 'tree',
                'model': model.model,
                'arch': etree.tostring(xml_tree),
            })

            # Form View
            xml_form = etree.Element("form")
            form_sheet = etree.SubElement(xml_form, "sheet")
            form_group = etree.SubElement(form_sheet, "group")
            form_group2 = etree.SubElement(form_group, "group")

            form_group2.set("col", "4")
            index = 0
            for field in new_fields:
                field = etree.SubElement(form_group2, "field", name=field.name)
                index += 1
                if index % 4 == 0:
                    form_group2 = etree.SubElement(form_group, "group")
                    form_group2.set("col", "4")

            IrView.create({
                'name': '%s.form.view' % (model.model),
                'type': 'form',
                'model': model.model,
                'arch': etree.tostring(xml_form)
            })

            menu_name = self.menu_name or model.model.title().replace(".", " ").replace("_", " ")

            # Action and Menu
            IrActionActWindow = self.env['ir.actions.act_window']
            action = IrActionActWindow.create({
                'name': menu_name,
                'res_model': model.model,
                'type': 'ir.actions.act_window'
            })

            self.env['ir.ui.menu'].create({
                'name': menu_name,
                'parent_id': self.parent_menu_id.id,
                'action': 'ir.actions.act_window,%d' % (action.id,)
            })

    def get_model(self, sheet):
        '''This method will check that model is already exist or not'''
        sheet_name = sheet.name or ''
        model_name = sheet_name.replace('_', '.').lower().replace(' ', '.')
        IrModel = self.env['ir.model']
        model = IrModel.search([('model', '=', model_name)])

        if not model:
            model = IrModel.create({
                'model': "x_%s" % (model_name),
                'name': sheet_name,
            })
            # Access Right
            IrAccess = self.env['ir.model.access']
            access_name = 'access_'+(model.name).replace('.', '_')
            IrAccess.create({
                'name': access_name,
                'model_id': model.id,
                'perm_read': True,
                'perm_write': True,
                'perm_create': True,
                'perm_unlink': True,
                })
        return model
