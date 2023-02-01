from mec_energia import settings

MEC_ENERGIA_URL = settings.MEC_ENERGIA_URL

def template_email_first_access(user_name, link_first_access_password):
    title = 'Bem Vindo ao Mec Energia'

    message = f'''
        <h2>{user_name}</h2>

        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas facilisis mauris nisi, id fringilla odio vulputate eget.
        Nullam facilisis, massa non euismod malesuada, nisi justo maximus odio, et finibus augue magna id ipsum.</p>

        <p>{link_first_access_password}</p>
    '''

    return (title, message)

def template_email_recovery_password(user_name, link_reset_password_page):
    title = 'Recuperação de senha Mec Energia'

    message = f'''
        <h3>Olá {user_name},</h3>

        <p>Foi solicitado a recuperação da sua senha de acesso ao sistema <a href="{MEC_ENERGIA_URL}">MEC Energia</a>.</p>

        <p>Para criar sua nova senha, clique no link abaixo:</p>
        <p>{link_reset_password_page}</p>

        <p>Se você não solicitou a recuperação da senha, ignore esta mensagem.</p>

        <p>Atenciosamente,</p>

        <p>Equipe MEC Energia</p>
    '''

    return (title, message)