import re

def validateDriver(first, last, ID, phone, email):
    if not first:
        return "First name can't be empty"
    if not last:
        return "Last name can't be empty"
    if not ID:
        return "ID can't be empty"
    if not phone:
        return "Phone number can't be empty"
    if not email:
        return "Email can't be empty"
    
    if not validateEmail(email):   
        return "Enter a valid email address"
    
    return True

def validateEmail(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False
    return True

def validateCab(model, color, regno):
    if not model:
        return "Car model can't be empty"
    if not color:
        return "Car color can't be empty"
    if not regno:
        return "Car registeration can't be empty"
    
    return True 