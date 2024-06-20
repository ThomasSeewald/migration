# -*- coding: utf-8 -*-

import base64
from datetime import datetime
from lxml import etree
import xlrd

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

ROW_FIELD = 0
ROW_DUMMY = 1
ROW_FROM_IMPORT = 2
FIELD_PREFIX = "x_"

MAP_CTYPE = {
    0: '',
    1: 'char',
    2: 'float',
    3: 'date',
    4: 'boolean',
}


class IrModelImportWizard(models.TransientModel):
    _name = 'ir.model.import.wizard'
    _description = "Import Wizard"

    file_name = fields.Binary(string="Select File")
    is_create_new_field = fields.Boolean("Create New Field", help="Create new fields in given model if field doesn't exist.")

    def read_data(self):
        if self.file_name:
            try:
                book = xlrd.open_workbook(file_contents=base64.decodebytes(self.file_name))
            except Exception as e:
                raise ValidationError(str(e))

            for sheet in book.sheets():
                model = self.get_model(sheet)
                if model:
                    self.validate_sheet(sheet)
                    # Check existing fields
                    # Add New Fields
                    if self.is_create_new_field:
                        index_of_new_fields = self.get_new_fields_index(model, sheet)
                        if index_of_new_fields:
                            new_fields = self.add_fields(sheet, model, index_of_new_fields)
                            self.add_fields_in_views(sheet, model, new_fields)

                    self.import_data(sheet, model)
                    return {'type': 'ir.actions.client', 'tag': 'reload'}
                else:
                    raise ValidationError(_("Given name in spreadsheet does not exist as model !!!"))
        else:
            raise ValidationError(_('Please Select File'))

    def _get_possible_field_name(self, sheet, col, row=ROW_FIELD):
        orig_field_name = sheet.cell_value(row, col)
        _field_name = orig_field_name.replace(' ', '_')
        prefix_name = "%s%s" % (FIELD_PREFIX, orig_field_name.replace(' ', '_').lower())
        return [orig_field_name, _field_name, prefix_name]

    def get_new_fields_index(self, model, sheet):
        existing_field_names = model.field_id.mapped("name")

        index_of_new_fields = []
        for col in range(0, sheet.ncols):
            field_names = self._get_possible_field_name(sheet, col)
            if not (set(field_names) & set(existing_field_names)):
                index_of_new_fields.append(col)
        return index_of_new_fields

    def validate_sheet(self, sheet):
        if sheet.row(0)[0].value == '':
            raise ValidationError(
                _('''First Row will be considered as Field Name, so Field Name is required for all columns.'''))
        elif sheet.row(1)[0].value == '':
            raise ValidationError(
                _('''Second Row will be considered as Dummy Data, we will identify datatype from this row.
                    So you must enter the dummy data in each column.'''))

    def get_model(self, sheet):
        '''This method will check that model is already exist or not'''
        sheet_name = sheet.name or ''
        model_name = sheet_name.replace('_', '.').lower().replace(' ', '.')
        IrModel = self.env['ir.model']
        model = IrModel.search([('model', '=', model_name)])
        return model

    def add_fields(self, sheet, model, index_of_new_fields):
        if not index_of_new_fields:
            return
        IrModelFields = new_fields = self.env['ir.model.fields']

        for col in index_of_new_fields:
            vals = {}
            field, _, field_name = self._get_possible_field_name(sheet, col)
            cell = sheet.row(ROW_DUMMY)[col]
            ctype = cell.ctype
            field_type = MAP_CTYPE.get(ctype, 'Char')
            if ctype == 3:
                dt = self._get_correct_date(sheet, cell.value)
                field_type = self._get_date_type(dt)

            vals.update({
                'ttype': field_type,
                'name': field_name,
                'field_description': field.title(),
                'store': True,
                'copied': False,
                'model_id': model.id,
                'state': 'manual',
            })
            new_fields += IrModelFields.create(vals)
        return new_fields

    def add_fields_in_views(self, sheet, model, new_fields):
        if not new_fields:
            return
        IrViews = self.env['ir.ui.view']
        new_view_name = 'sheet_import_field.%s.added.bysystem' % (model.model)

        # 1. Check Notebook > Page [vp_custom_import] ?
        #       Already added by Us
        # 2. Check Notebook ?
        #       There is atleast one page
        # 3. Add Notebook
        #       Add Page

        # Check for existing views added by us
        existing_view = IrViews.search(
            [('model', '=', model.model), ('name', 'ilike', new_view_name),
             ('type', '=', 'form'), ('mode', '=', 'extension')], limit=1)
        if existing_view:
            # 1. Already we added our own custom imported fields
            eview = etree.fromstring(existing_view.arch)
            if len(eview.findall(".//xpath")) > 0:
                xpath = eview.findall(".//xpath//page")[0]
                form_group = etree.SubElement(xpath, "group")
                for n_field in new_fields:
                    n_field = etree.SubElement(form_group, "field", name=n_field.name)

            str_xml = etree.tostring(eview)
            existing_view.write({
                'arch': str_xml,
                'arch_base': str_xml,
            })
        else:
            view = IrViews.search(
                [('model', '=', model.model),
                 ('type', '=', 'form'), ('mode', '=', 'primary'), ('inherit_id', '=', False)], limit=1)

            if not view:
                raise ValidationError(_("Any view not found for %s model") % (model.model))

            data = etree.Element("data")
            xpath = etree.SubElement(data, 'xpath')

            eview = etree.fromstring(view.arch)
            if len(eview.findall(".//notebook")) > 0:
                # 2. Notebook already avaialble
                xpath.set("expr", ".//notebook")
                xpath.set("position", "inside")
                parent = xpath
            else:
                # 3. Add Notebook and Page
                if len(eview.findall('.//sheet')) > 0:
                    xpath.set("expr", "//sheet")
                else:
                    xpath.set("expr", "//form")
                xpath.set("position", "inside")
                notebook = etree.SubElement(xpath, 'notebook')
                parent = notebook
            page = etree.SubElement(parent, 'page', string="Imported Fields", name="vp_custom_import")

            form_group = etree.SubElement(page, "group")
            for n_field in new_fields:
                n_field = etree.SubElement(form_group, "field", name=n_field.name)

            str_xml = etree.tostring(data)

            IrViews.create({
                'name': new_view_name,
                'type': 'form',
                'model': model.model,
                'inherit_id': view.id,
                'mode': 'extension',
                'priority': 1,
                'arch': str_xml,
                'arch_base': str_xml,
            })

    def import_data(self, sheet, model):
        records = self.env[model.model]
        for row in range(ROW_FROM_IMPORT, sheet.nrows):
            vals = {}
            for col in range(0, sheet.ncols):
                field_names = self._get_possible_field_name(sheet, col)
                field_value = sheet.cell_value(row, col)
                lst_field = model.field_id.filtered(lambda f: f.name in field_names)
                for lst in lst_field:
                    if lst.ttype == 'many2one':
                        rec = self.env[lst.relation].browse([int(field_value)])
                        field_value = rec.id
                        vals.update({lst.name: rec.id})
                    elif lst.ttype in ['date', 'datetime']:
                        field_value = self._get_correct_date(sheet, field_value)
                        if lst.ttype == 'date':
                            field_value = fields.Date.to_string(field_value)
                        elif lst.ttype == 'datetime':
                            field_value = fields.Datetime.to_string(field_value)
                    elif lst.ttype == 'boolean':
                        field_value = bool(field_value)
                    vals.update({lst.name: field_value})
            if vals:
                try:
                    records += self.env[model.model].create(vals)
                except Exception as e:
                    raise UserError("LINE #%s:: %s\n\n%s" % (row + 1, "   ".join(map(str, sheet.row(row))), str(e)))
        return records

    def _get_correct_date(self, sheet, value):
        return datetime(*xlrd.xldate_as_tuple(value, sheet.book.datemode))

    def _get_date_type(self, dt):
        if dt and isinstance(dt, datetime) and dt.hour > 0 or dt.minute > 0 or dt.second > 0:
            return 'datetime'
        return 'date'
