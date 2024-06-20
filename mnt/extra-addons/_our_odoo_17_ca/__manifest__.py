{
    'name': 'Google Drive Integration for CRM Leads',
    'version': '1.0',
    'summary': 'Integrate Google Drive API with CRM Leads',
    'description': """
        This module integrates Google Drive API with CRM Leads in Odoo.
        It allows users to retrieve student application and contract PDFs from Google Drive.
    """,
    'author': 'Your Name',
    'website': 'https://www.example.com',
    'depends': ['crm'],
    'data': [
        'views/crm_lead_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
