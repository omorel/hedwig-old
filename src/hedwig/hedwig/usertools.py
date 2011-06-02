import re
import constants 

def is_username_valid(username):
    result = re.match(constants.USERNAME_REGEXP_PATTERN, username)
    
    if(result):
        return True
    else: 
        return False
    
def is_password_valid(password):
    length = len(password)
    if(length > constants.PASSWORD_MAX_LENGTH or length < constants.PASSWORD_MIN_LENGTH):
        return False 
    
    result = re.match("[0-9]", password)
    if(len(result.groups) < constants.PASSWORD_MIN_NUMBERS): 
        return False
    
    result = re.match("[A-Z]", password)
    if(len(result.groups) < constants.PASSWORD_MIN_CAPITAL_LETTERS): 
        return False
    
    return True