from datetime import datetime
import mailtrap as mt
from config import settings

class MailService:
    def __init__(self, token: str):
        self.client = mt.MailtrapClient(token=token)
        self.sender = mt.Address(email="mailtrap@demomailtrap.com", name="Mailtrap Test")
        self.reg_template_uuid = "0fb26393-1adc-4508-993a-149a20b7f501"
        self.order_template_uuid = "ecdcc387-0387-4f9b-94cb-10dbdcb6c46f"

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
    
    def send_order_confirmation_email(self, email: str, user_name: str, order_id: str, order_date: datetime, country: str, city: str, address: str, user_email: str):
        order_date_str = order_date.strftime('%Y-%m-%d %H:%M:%S')
        mail = mt.MailFromTemplate(
            sender=self.sender,
            to=[mt.Address(email=email)],
            template_uuid=self.order_template_uuid,
            template_variables={
                "user_name": user_name,
                "order_id": order_id,
                "order_date": order_date_str,
                "country": country,
                "city": city,
                "address": address,
                "user_email": user_email
            }
        )
        self.client.send(mail)

mail_app = MailService(token=settings.MAILTRAP_TOKEN)