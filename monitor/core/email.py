from O365 import Message
from decouple import config

from core.errors import EmailError


class SendMail:
    def __init__(self):
        """
        Inicializa classe app recebendo informações do arquivo .env e inicia conexão
        """
        self.user = config('EMAIL_USER')
        self.pwd = config('EMAIL_PASS')
        self.to_email = config('EMAIL_TO')

    def send(self, subject, body, to=None):
        """
        Envia email
        :param subject: titulo de mensagem
        :param body: corpo do email
        :return: objeto de email
        """
        m = Message(auth=(self.user, self.pwd))
        emails = self.to_email if to is None else to

        for i in emails.split(';'):
            m.addRecipient(i)
        m.setSubject(subject)
        m.setBodyHTML(body)
        try:
            m.sendMessage()
        except Exception as e:
            raise EmailError(f'Erro ao enviar o email. Erro: {e}')
