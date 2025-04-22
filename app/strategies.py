from fuzzywuzzy import fuzz
from app.db.models import User

def string_compare(str1:str):
    def compare(usr:User):
        return fuzz.ratio(str1, str(usr.username)) > 20
    return compare