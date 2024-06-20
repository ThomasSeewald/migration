# import pandas as pd
# import base64

# from odoo import models, api, fields
# class Lead(models.Model):
#     _inherit = 'crm.lead'

#     x_stud_name = fields.Char(string="Student Name")
#     x_stud_vorname = fields.Char(string="Student First Name")
#     x_stud_hausnummer = fields.Char(string="House Number")
#     x_stud_geburtsdatum = fields.Date(string="Birth Date")
#     x_stud_geburtsort = fields.Char(string="Birth Place")
#     x_stud_geschlecht = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
#     x_language_level_german = fields.Char(string="German Language Level")
#     x_language_certificate = fields.Char(string="Language Certificate")
#     x_Agent = fields.Char(string="Agent")
#     x_agents = fields.Char(string="Agents")
#     x_email_gmail = fields.Char(string="Gmail")
#     x_employer = fields.Char(string="Employer")
#     x_employer_missing_documents = fields.Char(string="Employer Missing Documents")
#     x_GDrivePath = fields.Char(string="Google Drive Path")
#     x_identity = fields.Char(string="Identity")
#     x_HWKIHK_Vertrag = fields.Char(string="HWKIHK Contract")
#     x_Interview_Date = fields.Date(string="Interview Date")
#     x_komplette_pdf = fields.Binary(string="Complete PDF")
#     x_missing_ds = fields.Char(string="Missing Documents")
#     x_motivation_text = fields.Text(string="Motivation Text")
#     x_our_provision = fields.Float(string="Our Provision")
#     x_pass_photo = fields.Binary(string="Passport Photo")
#     x_rechnung_erstellt = fields.Boolean(string="Invoice Created")
#     x_school = fields.Char(string="School")
#     x_sendungsnummer_ausbildungsvertrag_aag = fields.Char(string="Shipment Number of Training Contract")
#     x_Typus = fields.Char(string="Type")
#     x_Unterstuetzungsdocument = fields.Boolean(string="Support Document")
#     x_warten_auf_Bewerbungen = fields.Boolean(string="Waiting for Applications")
#     x_zweite_zahlung = fields.Float(string="Second Payment")
    


#     @api.model
#     def load_data_from_excel(self):
#         # Define the path to the Excel file
#         file_path = '/mnt/extra-addons/LeadOpportunity.xlsx'
        
#         # Read the Excel file
#         data = pd.read_excel(file_path)

#         # Iterate over each row and create a lead record
#         for index, row in data.iterrows():
#             self.create({
#                 'name': row['name'],
#                 'x_stud_name': row['x_stud_name'],
#                 'x_stud_vorname': row['x_stud_vorname'],
#                 'x_stud_hausnummer': row['x_stud_hausnummer'],
#                 'x_stud_geburtsdatum': row['x_stud_geburtsdatum'],
#                 'x_stud_geburtsort': row['x_stud_geburtsort'],
#                 'x_stud_geschlecht': row['x_stud_geschlecht'],
#                 'x_language_level_german': row['x_language_level_german'],
#                 'x_language_certificate': row['x_language_certificate'],
#                 'x_employer_missing_documents': row['x_employer_missing_documents'],
#                 'x_GDrivePath': row['x_GDrivePath'],
#                 'x_identity': row['x_identity'],
#                 'x_HWKIHK_Vertrag': row['x_HWKIHK_Vertrag'],
#                 'x_Interview_Date': row['x_Interview_Date'],
#                 'x_komplette_pdf': row['x_komplette_pdf'],
#                 'x_missing_ds': row['x_missing_ds'],
#                 'x_motivation_text': row['x_motivation_text'],
#                 'x_our_provision': row['x_our_provision'],
#                 'x_pass_photo': row['x_pass_photo'],
#                 'x_rechnung_erstellt': row['x_rechnung_erstellt'],
#                 'x_school': row['x_school'],
#                 'x_sendungsnummer_ausbildungsvertrag_aag': row['x_sendungsnummer_ausbildungsvertrag_aag'],
#                 'x_Typus': row['x_Typus'],
#                 'x_Unterstuetzungsdocument': row['x_Unterstuetzungsdocument'],
#                 'x_warten_auf_Bewerbungen': row['x_warten_auf_Bewerbungen'],
#                 'x_zweite_zahlung': row['x_zweite_zahlung'],
#                 'x_email_gmail': row['x_email_gmail'],
#                 'x_Agent': row['x_Agent'],
#                 'x_agents': [(6, 0, [int(x) for x in str(row['x_agents']).split(',')])],
#                 'x_color': row['x_color'],
#                 'x_contact_name': row['x_contact_name'],
#                 'x_country_id': row['x_country_id'],
#                 'x_employer': row['x_employer'],
#                 'x_phone_mobile_search': row['x_phone_mobile_search'],
#                 'x_phone': row['x_phone'],
#                 'x_priority': row['x_priority'],
#                 'x_state_id': row['x_state_id'],
#                 'x_stage_id': row['x_stage_id'],
#                 'x_tag_ids': [(6, 0, [int(x) for x in str(row['x_tag_ids']).split(',')])],
#                 'x_type': row['x_type'],
#                 'x_user_id': row['x_user_id'],
#             })

#     def action_import_excel(self):
#         self.load_data_from_excel()


###########
import base64
import pandas as pd
from odoo import models, api, fields
from odoo.exceptions import UserError, AccessError

class Lead(models.Model):
    _inherit = 'crm.lead'#child 
    
    
   # _name='crm.lead'=parent/father

    x_stud_name = fields.Char(string="Student Name")
    x_stud_vorname = fields.Char(string="Student First Name")
    x_stud_hausnummer = fields.Char(string="House Number")
    x_stud_geburtsdatum = fields.Date(string="Birth Date")
    x_stud_geburtsort = fields.Char(string="Birth Place")
    x_stud_geschlecht = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    x_language_level_german = fields.Char(string="German Language Level")
    x_language_certificate = fields.Char(string="Language Certificate")
    x_Agent = fields.Char(string="Agent")
    x_agents = fields.Char(string="Agents")
    x_email_gmail = fields.Char(string="Gmail")
    x_employer = fields.Char(string="Employer")
    x_employer_missing_documents = fields.Char(string="Employer Missing Documents")
    x_GDrivePath = fields.Char(string="Google Drive Path")
    x_identity = fields.Char(string="Identity")
    x_HWKIHK_Vertrag = fields.Char(string="HWKIHK Contract")
    x_Interview_Date = fields.Date(string="Interview Date")
    x_komplette_pdf = fields.Binary(string="Complete PDF")
    x_missing_ds = fields.Char(string="Missing Documents")
    x_motivation_text = fields.Text(string="Motivation Text")
    x_our_provision = fields.Float(string="Our Provision")
    x_pass_photo = fields.Binary(string="Passport Photo")
    x_rechnung_erstellt = fields.Boolean(string="Invoice Created")
    x_school = fields.Char(string="School")
    x_sendungsnummer_ausbildungsvertrag_aag = fields.Char(string="Shipment Number of Training Contract")
    x_Typus = fields.Char(string="Type")
    x_Unterstuetzungsdocument = fields.Boolean(string="Support Document")
    x_warten_auf_Bewerbungen = fields.Boolean(string="Waiting for Applications")
    x_zweite_zahlung = fields.Float(string="Second Payment")

    @api.model
    def load_data_from_excel(self, file_path):
        try:
            data = pd.read_excel(file_path)
        except Exception as e:
            raise UserError(f"Error reading Excel file: {e}")

        for index, row in data.iterrows():
            try:
                agents = [(6, 0, [int(x) for x in str(row['x_agents']).split(',') if x.isdigit()])]
            except ValueError:
                agents = False

            lead_vals = {
                'name': row.get('name'),
                'x_stud_name': row.get('x_stud_name'),
                'x_stud_vorname': row.get('x_stud_vorname'),
                # Add other fields here
                'x_agents': agents,
            }

            lead = self.create(lead_vals)
            # Add any additional processing or error handling here

    def action_import_excel(self):
        file_path = '/mnt/extra-addons/LeadOpportunity.xlsx'
        self.load_data_from_excel(file_path)