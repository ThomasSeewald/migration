# -*- coding: utf-8 -*-

{
    "name": "Add New Fields & Data from Worksheet",
    "version": "17.0.1.0.0",
    "sequence": 0,
    "author": "VperfectCS",
    "maintainer": "VperfectCS",
    "category": "Extra Tools",
    "summary": """
Add New Fields in the Model, Form View Dynamically from the Worksheet Upload.
""",
    "description": """
This module adds the possibilities to
=================================================================================================
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
    "depends": ["base"],
    "external_dependencies": {"python": ["xlrd"]},
    "data": ["security/ir.model.access.csv", "wizard/sheet_import_views.xml"],
    "images": ["static/description/banner.png"],
    "demo": [],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": 49,
    "currency": "EUR",
}
