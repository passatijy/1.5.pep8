# from io import StringIO
import email
import smtplib
import imaplib
from email.mime.text import MIMEText
# from email.MIMEMultipart import MIMEMultipart
from email.mime.multipart import MIMEMultipart


class Mailconnector():
    def __init__(self, smtp_server, imap_server, login, password):
        self.smtp_server = smtp_server
        self.imap_server = imap_server
        self.login = login
        self.password = password

    def send_mail(self, send_from, rcpt_to, send_subject, send_message):
        '''send mail'''
        # send message
        self.msg = MIMEMultipart()
        self.msg['From'] = send_from
        self.msg['To'] = ', '.join(rcpt_to)
        self.msg['Subject'] = send_subject
        self.msg.attach(MIMEText(send_message))
        # msg_sender = smtplib.SMTP(GMAIL_SMTP, 587)
        msg_sender = smtplib.SMTP(self.smtp_server, 25)
        # identify ourselves to smtp gmail client
        msg_sender.ehlo()
        # secure our email with tls encryption
        msg_sender.starttls()
        # re-identify ourselves as an encrypted connection
        msg_sender.ehlo()
        msg_sender.login(self.login, self.password)
        msg_sender.sendmail(self.login, rcpt_to, self.msg.as_string())
        # send end
        return msg_sender.quit()

    def recieve_mail(self, header):
        '''recieve mail'''
        mail = imaplib.IMAP4_SSL(self.imap_server)
        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        mail.logout()
        # end recieve
        return email_message


SMTP_SERVER = "smtp.yandex.ru"
IMAP_SERVER = "imap.yandex.ru"
LOGIN = ''
PASSWORD = ''

HEADER = None

if __name__ == '__main__':
    repeat = True
    mailconnector = Mailconnector(SMTP_SERVER, IMAP_SERVER, LOGIN, PASSWORD)
    while repeat:
        command = input('Введите команду \
            (s,r,q; s - send mail, r - recieve mail, q - выход) ')
        if command == 'q':
            repeat = False
            break
        elif command == 's':
            print('Будем отправлять почту')
            rcpt = input('Кому: ')
            sbjct = input('Заголовок письма: ')
            body = input('Введите сообщение: ')
            print('Отправляем почту для:', rcpt, ' \
                Заголовок:', sbjct, ' сообщение:', body)
            send_mail_result = mailconnector.send_mail(
                LOGIN, rcpt, sbjct, body)
            print('Результат отправки:', send_mail_result)
        elif command == 'r':
            print('Будем получать почту')
            recieve_mail_result = mailconnector.recieve_mail(
                HEADER)
            print('Результат получения почты:', recieve_mail_result)
