import config_email

if __name__ == "__main__":
    destinatario = "medeiros0441@hotmail.com"
    assunto = "Assunto do Email"
    NomeCliente = "Nome do Cliente"
    TextIntroducao = "Texto de Introdução"

    config_email.enviar_email(destinatario, assunto, NomeCliente, TextIntroducao)
