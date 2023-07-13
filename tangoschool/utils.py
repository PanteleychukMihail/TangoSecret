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
            del(user_menu[0:4])
            context['menu'] = user_menu

        if self.request.user.is_authenticated and self.request.user.is_staff:
            user_menu.pop(5)
        context['menu'] = user_menu
        return context
