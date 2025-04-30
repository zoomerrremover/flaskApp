from fuzzywuzzy import fuzz
from app.db.models import User
from email_validator import validate_email, EmailNotValidError

def string_compare(str1:str):
    def compare(usr:User):
        return fuzz.ratio(str1, str(usr.username)) > 20
    return compare

def is_valid_email(email):
    try:
        emailinfo = validate_email(email, check_deliverability=False)
        return True, emailinfo.normalized
    except EmailNotValidError as e:
        return False, str(e)
