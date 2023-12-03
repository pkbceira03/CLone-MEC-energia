def test_verifica_formato_email():
    email = "usuario@dominio.com"
    assert verifica_formato_email(email) == True

    email_invalido = "email_invalido"
    assert verifica_formato_email(email_invalido) == False

def test_verifica_servidor_email():
    email_valido = "usuario@dominio.com"
    assert verifica_servidor_email(email_valido) == True

    email_invalido = "usuario@dominioinexistente.com"
    assert verifica_servidor_email(email_invalido) == False

def test_verifica_email_completo():
    email_valido = "usuario@dominio.com"
    assert verifica_email_completo(email_valido) == True

    email_invalido = "usuario@dominioinexistente.com"
    assert verifica_email_completo(email_invalido) == False

    email_invalido_formato = "email_invalido"
    assert verifica_email_completo(email_invalido_formato) == False
