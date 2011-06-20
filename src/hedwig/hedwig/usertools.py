import re
import constants 
import random
import string
import hashlib

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
    
	result = re.findall("[0-9]", password)
	if(len(result) < constants.PASSWORD_MIN_NUMBERS): 
		return False		
    
	result = re.findall("[A-Z]", password)
	if(len(result) < constants.PASSWORD_MIN_CAPITAL_LETTERS): 
		return False
    
	return True

def is_email_valid(email):
	return True 

def generate_salt(length = constants.USER_SALT_LENGTH, possible_values = string.ascii_letters): 
	random.seed()
	salt = ''
	for i in range(length):
		salt += random.choice(possible_values)
	return salt
	
def create_password(username, salt, email, password): 
	return hashlib.sha256(username + salt + email + password).hexdigest()
	