import re

#Валидация email используемая в person_service
class EmailService:
    @staticmethod
    def validate_email_format(email: str):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValueError("Invalid email format")