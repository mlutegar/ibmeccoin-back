from django.core.mail import send_mail
from django.conf import settings

try:
    send_mail('Assunto do E-mail de Teste - Django','Este é o corpo da mensagem de teste.', settings.DEFAULT_FROM_EMAIL, ['mlutegar@gmail.com'], fail_silently=False,)
    print("E-mail enviado com sucesso (verifique a caixa de entrada e spam)!")
except Exception as e:
    print(f"Erro ao enviar e-mail: {e}")

quit() # Para sair do shell