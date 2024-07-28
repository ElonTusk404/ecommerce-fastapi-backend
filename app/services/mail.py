import mailtrap as mt
from config import settings

class MailService:
    def __init__(self, token: str):
        self.client = mt.MailtrapClient(token=token)
        self.sender = mt.Address(email="mailtrap@demomailtrap.com", name="Mailtrap Test")
        self.reg_template_uuid = "0fb26393-1adc-4508-993a-149a20b7f501"

    def send_registration_email(self, email: str, name: str):
        mail = mt.MailFromTemplate(
            sender=self.sender,
            to=[mt.Address(email=email)],
            template_uuid=self.reg_template_uuid,
            template_variables={
                "company_info_name": "Ecommerce App",
                "name": name,
                "company_info_address": "221B Baker Street",
                "company_info_city": "London",
                "company_info_zip_code": "NW1 6XE",
                "company_info_country": "United Kingdom"
            }
        )
        self.client.send(mail)

mail_app = MailService(token=settings.MAILTRAP_TOKEN)