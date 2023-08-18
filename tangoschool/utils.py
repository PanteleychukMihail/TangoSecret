import openpyxl
from django.core.mail import EmailMessage
from io import BytesIO

from .models import *

menu = [{'title': 'Новый Ученик', 'url_name': 'add_student'},
        {'title': 'Список учеников', 'url_name': 'users_list'},
        {'title': 'Создать занятие', 'url_name': 'add_lesson'},
        {'title': 'Создать практику', 'url_name': 'add_practice'},
        {'title': 'Прошлые уроки', 'url_name': 'lessons_view'},
        {'title': 'Редактировать профиль', 'url_name': 'user_update'}
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu = []

        if self.request.user.is_authenticated and not self.request.user.is_staff:
            del (user_menu[0:4])
            context['menu'] = user_menu

        if self.request.user.is_authenticated and self.request.user.is_staff:
            user_menu.pop(5)
        context['menu'] = user_menu
        return context


def create_and_send_excel_report():
    # Создаем новый Excel-файл
    wb = openpyxl.Workbook()
    ws = wb.active

    # Добавляем заголовки
    ws.append(['Фамилия', 'Имя', 'Баланс'])

    # Заполняем данными остатков занятий для студентов
    students = Student.objects.all()
    for student in students:
        ws.append([student.last_name, student.first_name, student.student_balance.balance])

    # Сохраняем файл в памяти
    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)

    # Отправляем письмо с Excel-файлом на указанную почту
    subject = 'Отчет по остаткам занятий'
    message = 'Пожалуйста, найдите прикрепленный Excel-файл с остатками занятий.'
    from_email = 'panteleychukmihail@gmail.com'
    recipient_list = ['kelton@kelton.com.ua']
    file_name = 'report.xlsx'

    email = EmailMessage(subject, message, from_email, recipient_list)
    email.attach(file_name, excel_file.read(), 'application/vnd.malformations-office document.spreadsheet.sheet')
    email.send()

    # Закрываем файл
    excel_file.close()
