import random

from django.core.mail import send_mail, BadHeaderError


# def generate(key=None, length=None):
#     """Генерация кода"""
#     if key is None:
#         key = ''
#     if length is None:
#         length = 32
#     digits = "0123456789"
#     letters = "abcdefghijklmnopqrstuvwxyz"
#     uletters = letters.upper()
#     blank = digits + letters + uletters + key
#     lst = list(blank)
#     random.shuffle(lst)
#     code = ''.join([random.choice(lst) for x in range(length)])
#     return code
#
#
# def send_email(email, code):
#     """Отправка кода на email"""
#     subject = 'Код подтверждения'
#     message = 'Введите этот код для подтверждения смены email: {}'.format(code)
#     try:
#         send_mail(subject, message, 'robot@djangochannel.com', [email])
#         return True
#     except BadHeaderError:
#         return False


def send_mail_feedback(user):
    """Отправка email о новом запросе в поддержку"""
    subject = 'Новый запрос в поддержку'
    message = 'Здравствуйте, пользователь {}, отправил запрос в поддержку'.format(user)
    try:
        send_mail(subject, message, 'dimmoon@mail.ru', ['dimmoon@mail.ru'])
        return True
    except BadHeaderError:
        return False
    # subject = 'Новый запрос в поддержку'
    # message = 'Здравствуйте, пользователь {}, отправил запрос в поддержку'.format(user)
    # try:
    #     send_mail(subject, message, 'hamell1987@gmail.com', ['hamell1987@gmail.com'])
    #     return True
    # except BadHeaderError:
    #     return False
