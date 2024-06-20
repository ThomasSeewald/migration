import requests
from odoo import models, fields, api
from base64 import encodebytes
from datetime import datetime, timedelta

class GoogleOAuth(models.Model):
    _name = 'google.oauth'

    user_id = fields.Many2one('res.users', string='User')
    refresh_token = fields.Char(string='Refresh Token')
    access_token = fields.Char(string='Access Token')
    expires_at = fields.Datetime(string='Token Expiration Time')

    @api.model
    def refresh_access_token(self):
        oauth_record = self.env['google.oauth'].search([('user_id', '=', self.env.user.id)], limit=1)
        if oauth_record:
            if oauth_record.expires_at < datetime.now():
                # Token is expired, refresh it
                new_access_token, new_expires_in = self._refresh_token(oauth_record.refresh_token)
                new_expires_at = datetime.now() + timedelta(seconds=new_expires_in)
                oauth_record.write({'access_token': new_access_token, 'expires_at': new_expires_at})
                return new_access_token
            else:
                # Token is still valid, return it
                return oauth_record.access_token
        else:
            return False

    def _refresh_token(self, refresh_token):
        # Make a request to the token endpoint to refresh the token
        token_url = "https://oauth2.googleapis.com/token"
        client_id = "672100355677-4r7959i133hcq9pkhsubu61grf9unhqq.apps.googleusercontent.com"

        client_secret = "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"
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        response = requests.post(token_url, data=payload)
        token_data = response.json()
        return token_data.get('access_token'), token_data.get('expires_in')














class CrmLead(models.Model):
    _inherit = 'crm.lead'

    agent_folder_id = fields.Char(string='Agent Folder ID')
    student_folder_ids = fields.One2many('crm.lead.student.folder', 'crm_lead_id', string='Student Folders')
    attachments = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'crm.lead')], string='Attachments')

    def action_save_student_pdfs(self):
        for lead in self:
            for folder in lead.student_folder_ids:
                application_pdf_id = folder.application_pdf_id
                contract_pdf_id = folder.contract_pdf_id
                if application_pdf_id and contract_pdf_id:
                    application_pdf_content = self._get_google_drive_file_content(application_pdf_id)
                    contract_pdf_content = self._get_google_drive_file_content(contract_pdf_id)
                    self._save_pdf_as_attachment(application_pdf_content, 'Application.pdf', lead)
                    self._save_pdf_as_attachment(contract_pdf_content, 'Contract.pdf', lead)
                    
    # def _get_access_token(self):
    #     # Token details
    #     refresh_token = "your_refresh_token"  # Replace "your_refresh_token" with the actual refresh token
    #     client_id = "672100355677-4r7959i133hcq9pkhsubu61grf9unhqq.apps.googleusercontent.com"  # Use the provided client ID
    #     client_secret = "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"  # Use the provided client secret
    #     refresh_url = "https://oauth2.googleapis.com/token"

    #     # Prepare refresh data
    #     refresh_data = {
    #         "client_id": client_id,
    #         "client_secret": client_secret,
    #         "refresh_token": refresh_token,
    #         "grant_type": "refresh_token"
    #     }

    #     # Request new access token
    #     response = requests.post(refresh_url, data=refresh_data)
    #     response.raise_for_status()
    #     return response.json()["access_token"]

    def _get_google_drive_file_content(self, file_id):
        # Static value for the access token
        #access_token = "ya29.a0AXooCgvMGMvBOm4h7cpUa1WXwmSXw_lAFCJUb5AQ1gLtbbg_EvRMkQNdugYKjwoBURnGPC23s8q1H5ExjEIXUlk9u5cBH98sbDN_12JQRkR0PiUcUeGJqpCZvccJDhj-QtAhBjlfH0Brt8r7iH48wnttNtTroiw1FQaCgYKAcISARASFQHGX2Mi1cxu4dTaJMBP74j4li-1fw0169"
        # access_token=self._get_access_token()
        access_token = self.env['google.oauth'].refresh_access_token()

        url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for non-2xx status codes
        return response.content

 
    def _save_pdf_as_attachment(self, pdf_content, pdf_name, lead):
    # Encode the PDF content to base64
        encoded_pdf_content = encodebytes(pdf_content)

        # Create the attachment record
        attachment = self.env['ir.attachment'].create({
            'name': f"{pdf_name}.pdf",  # Ensure the file name has the .pdf extension
            'type': 'binary',
            'datas': encoded_pdf_content,
            'res_model': 'crm.lead',
            'res_id': lead.id,
            'mimetype': 'application/pdf'  # Set the MIME type for PDF files
        })
    

class CrmLeadStudentFolder(models.Model):
    _name = 'crm.lead.student.folder'

    name = fields.Char(string='Name')
    application_pdf_id = fields.Char(string='Application PDF File ID')
    contract_pdf_id = fields.Char(string='Contract PDF File ID')
    crm_lead_id = fields.Many2one('crm.lead', string='CRM Lead')
