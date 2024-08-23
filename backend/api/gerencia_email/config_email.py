import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
from .gerar_html_email import corpo_email
from django.conf import settings


def is_valid_email(email):
    # Expressão regular para validar email
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_pattern, email)


def enviar_email(
    destinatario,
    assunto,
    NomeCliente,
    TextIntroducao,
    TextContainer2="",
    TextContainer3="",
    btn_vermais=False,
):
    # Lista de contas de e-mail que você deseja alternar em caso de problemas
    contas_email = [
        {"username": settings.username_email_1, "password": settings.password_email_1},
        {"username":settings.username_email_2, "password": settings.password_email_2},
    ]

    email_enviado = False  # Variável de controle para rastrear se o e-mail foi enviado

    for conta in contas_email:
        if email_enviado:
            break  # Se o e-mail já foi enviado, sair do loop

        smtp_username = conta["username"]
        smtp_password = conta["password"]

        # Configurações do email
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Criar objeto MIMEMultipart
        message = MIMEMultipart()
        message["From"] = smtp_username
        message["To"] = destinatario
        message["Subject"] = assunto

        # Gerar o corpo do email usando a função de geração de HTML
        html_body = corpo_email(
            NomeCliente, TextIntroducao, TextContainer2, TextContainer3, btn_vermais
        )

        # Adicionar o corpo do email (HTML)
        message.attach(MIMEText(html_body, "html"))

        # Configurar a conexão SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        try:
            # Efetuar login
            server.login(smtp_username, smtp_password)

            # Enviar o email
            server.sendmail(smtp_username, destinatario, message.as_string())
            print("Email enviado com sucesso!")
            email_enviado = True  # Definir a variável de controle para True
        except smtplib.SMTPDataError as e:
            error_code, error_message = e.smtp_code, e.smtp_error
            if (
                error_code == 550
                and b"Daily user sending quota exceeded" in error_message
            ):
                print(
                    "Limite diário de envio de e-mails atingido. Alternando para outra conta."
                )
            else:
                print(f"Erro ao enviar o email: {str(e)}")
        except Exception as e:
            print(f"Erro ao enviar o email: {str(e)}")
        finally:
            # Encerrar a conexão SMTP
            server.quit()

    if not email_enviado:
        print("Não foi possível enviar o email com nenhuma conta.")
