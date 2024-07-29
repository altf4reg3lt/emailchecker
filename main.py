import smtplib
import re
import dns.resolver
from datetime import datetime
from colorama import init, Fore, Style
import os
import time


# Initialize colorama
init(autoreset=True)

ascii_art = r""""


   :::::::::::       ::::    :::       :::::::::           :::        ::::::::       :::    :::       ::::::::::: 
         :+:           :+:+:   :+:            :+:          :+: :+:     :+:    :+:      :+:    :+:           :+:      
        +:+           :+:+:+  +:+           +:+          +:+   +:+    +:+             +:+    +:+           +:+       
       +#+           +#+ +:+ +#+          +#+          +#++:++#++:   :#:             +#++:++#++           +#+        
      +#+           +#+  +#+#+#         +#+           +#+     +#+   +#+   +#+#      +#+    +#+           +#+         
     #+#           #+#   #+#+#        #+#            #+#     #+#   #+#    #+#      #+#    #+#           #+#          
###########       ###    ####       #########       ###     ###    ########       ###    ###       ###########       
                                                 Email Validy Checker
"""



def is_valid_email(email):
    """
    Validate the email address syntax using regex.
    """
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def check_mx_record(domain):
    """
    Check if the domain has a valid MX (Mail Exchange) record.
    """
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout, dns.resolver.NoNameservers):
        return False

def smtp_check(email):
    """
    Check if the email address is valid by performing an SMTP check.
    """
    domain = email.split('@')[1]
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_record = mx_records[0].exchange
        mx_record = str(mx_record)
        
        server = smtplib.SMTP()
        server.connect(mx_record)
        server.helo(server.local_hostname)
        server.mail('your-email@example.com')
        code, message = server.rcpt(email)
        server.quit()
        
        if code == 250:
            return True
        else:
            return False
    except Exception:
        return False

def check_email(email):
    """
    Check if the email address is valid by checking its syntax, MX records, and performing an SMTP check.
    """
    if not is_valid_email(email):
        return False, "Invalid characters"
    
    domain = email.split('@')[1]
    
    if not check_mx_record(domain):
        return False, "Invalid MX records"
    
    if not smtp_check(email):
        return False, "SMTP check failed"
    
    return True, "Valid email"

def print_email_status(email, status, reason, checked_count, valid_count, invalid_count):
    """
    Print the email status in colorized format.
    """
    domain = email.split('@')[1]
    current_time = datetime.now().strftime("%H:%M %d.%m.%y")
    
    if status:
        status_text = f"{Fore.GREEN}VALID: TRUE"
        valid_count += 1
    else:
        status_text = f"{Fore.RED}VALID: FALSE - {reason}"
        invalid_count += 1
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(ascii_art)
    print(f"CMD  CHECKED: {checked_count}  VALID: {valid_count}  INVALID: {invalid_count}\n")
    print(f"{Fore.BLUE}{email} {Style.RESET_ALL} {status_text} {Style.RESET_ALL} DOMAIN: {Fore.YELLOW}{domain} {Style.RESET_ALL} DATE: {Fore.CYAN}{current_time}")
    return valid_count, invalid_count

def main():
    # File containing email addresses
    file_path = 'emails.txt'

    # Read emails from the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    checked_count = 0
    valid_count = 0
    invalid_count = 0

    for line in lines:
        line = line.strip()
        if line:
            # Extract email before the colon
            email = line.split(':')[0].strip()
            if email:
                checked_count += 1
                status, reason = check_email(email)
                valid_count, invalid_count = print_email_status(email, status, reason, checked_count, valid_count, invalid_count)
                  # Add delay for better visualization

if __name__ == "__main__":
    main()
