from .models import *

menu = [{'title': 'Добавить Ученика', 'url_name': 'add_student'},
        {'title': 'Список учеников', 'url_name': 'users_list'},
        {'title': 'Создать урок', 'url_name': 'add_lesson'},
        {'title': 'Список уроков', 'url_name': 'lessons_view'},
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
            user_menu.pop(4)
        context['menu'] = user_menu
        return context
