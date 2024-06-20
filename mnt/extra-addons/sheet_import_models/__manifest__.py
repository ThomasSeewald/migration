# -*- coding: utf-8 -*-

{
    "name": "Add New Models, Fields, Form/Tree Views from Worksheet",
    "version": "17.0.1.0.0",
    "sequence": 0,
    "author": "VperfectCS",
    "maintainer": "VperfectCS",
    "category": "Extra Tools",
    "summary": """
Add New Models, Fields, Form/Tree Views from Worksheet
""",
    "description": """
This module adds the possibilities to
=================================================================================================
- Add New Models
- Form and Tree views of that model
- Add New Menu, and system will bind the action and views
- Add New Fields into the new model from Worksheet
- Supported Field Types
    - Char (String/Text)
    - Boolean (True/False)
    - Integer
    - Float
    - Date
    - Datetime
- Import data from Worksheet.
""",
    "depends": ["sheet_import_field"],
    "external_dependencies": {"python": ["xlrd"]},
    "data": ["wizard/sheet_import_views.xml"],
    "images": ["static/description/banner.png"],
    "demo": [],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": 39,
    "currency": "EUR",
}
