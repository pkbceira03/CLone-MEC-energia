import re
import dns.resolver
import teste_verifica_email.py

def verifica_formato_email(email):
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(regex, email))

def verifica_servidor_email(email):
    dominio = email.split('@')[1]
    try:
        dns.resolver.resolve(dominio, 'MX')
        return True
    except:
        return False

def verifica_email_completo(email):
    return verifica_formato_email(email) and verifica_servidor_email(email)
