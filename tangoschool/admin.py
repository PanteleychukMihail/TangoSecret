from django import forms
from django.contrib import admin

from .models import *


class TrainerAdmin(admin.ModelAdmin):
    list_display = ('user_last_name', 'user_first_name', 'phone_number', 'email', 'experience')
    list_editable = ('phone_number', 'email', 'experience')
    ordering = ('experience',)
    search_fields = ('user_last_name',)
    list_select_related = ('user',)
    readonly_fields = ('user_first_name', 'user_last_name')

    def user_first_name(self, obj):
        return obj.user.first_name

    def user_last_name(self, obj):
        return obj.user.last_name

    user_first_name.short_description = 'Имя'
    user_last_name.short_description = 'Фамилия'


class StudentForm(forms.ModelForm):
    initial_balance = forms.IntegerField(label='Initial Balance', required=False)

    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_balance'].required = False


class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'level', 'is_active', 'get_balance', 'birth_day', 'phone_number',)
    list_editable = ('level', 'is_active')
    ordering = ('-is_active', '-level')
    search_fields = ('last_name',)
    list_filter = ("is_active", 'level')
    form = StudentForm

    def get_balance(self, obj):
        return obj.student_balance.balance

    def save_model(self, request, obj, form, change):
        initial_balance = form.cleaned_data.get('initial_balance')
        lesson_balance = form.cleaned_data.get('student_balance')
        if not lesson_balance:
            lesson_balance = Account.objects.create()
            lesson_balance.save()
            obj.student_balance = lesson_balance

            super().save_model(request, obj, form, change)

            if initial_balance:
                Operation.objects.create(
                    operation_type='buying',
                    lesson_balance=obj.student_balance,
                    amount=initial_balance
                )
        else:
            Operation.objects.create(
                operation_type='buying',
                lesson_balance=lesson_balance,
                amount=initial_balance
            )

        super().save_model(request, obj, form, change)

    get_balance.short_description = 'Остаток занятий'


class AccountAdmin(admin.ModelAdmin):
    list_display = ('students_list', 'balance')
    list_display_links = ('balance',)  # Делаем только поле balance кликабельным

    def students_list(self, obj):
        students = obj.students.all()
        student_names = ", ".join([str(student) for student in students])
        return student_names

    students_list.short_description = 'Студенты'  # Название колонки в админке
    students_list.admin_order_field = 'students__last_name'  # Сортировка по фамилии студента

    # fieldsets = (
    #     (None, {
    #         'fields': ('balance',),
    #     }),
    #     ('Студенты', {
    #         'fields': ('students',),
    #     }),
    # )


class OperationAdmin(admin.ModelAdmin):
    list_display = ('operation_type', 'student_name', 'amount', 'date', 'time')
    ordering = ('-date','-time')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_type', 'lesson_topic', 'level', 'date', 'time')
    list_editable = ('lesson_topic', 'level')
    ordering = ('-date', '-time')
    filter_horizontal = ("students", 'guests')
    list_filter = ("lesson_type", 'level')


admin.site.register(TrainerProfile, TrainerAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Guest)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Operation, OperationAdmin)

# class LessonAdmin(admin.ModelAdmin):
# def save_model(self, request, obj, form, change):
#     lesson = form.save(commit=False)
#
#     if change:  # Проверяем, является ли это изменением существующего объекта
#         old_lesson = Lesson.objects.get(pk=lesson.pk)  # Получаем старый объект урока
#
#         if old_lesson.lesson_type != lesson.lesson_type:  # Проверяем изменение типа урока
#             students = form.cleaned_data.get('students')
#
#             for student in students:
#                 count = 2 if form.cleaned_data.get(f'family_{student.pk}') else 1
#
#                 if old_lesson.lesson_type == 'full':
#                     student.lessons_balance += 0.5 * count  # Возвращаем 0.5 к балансу, если  тип был 'full'
#
#                 elif old_lesson.lesson_type == 'practice':
#                     student.lessons_balance -= 0.5 * count  # Возвращаем 1.0 к балансу, если  тип был 'practice'
#
#                 student.save()
#
#         old_students = old_lesson.students.all()
#         new_students = form.cleaned_data['students']
#
#         # Проверяем добавленных студентов
#         for student in new_students:
#             count = 2 if form.cleaned_data.get(f'family_{student.pk}') else 1
#             if student not in old_students:
#                 if lesson.lesson_type == 'full':
#                     student.lessons_balance -= 1 * count
#                 elif lesson.lesson_type == 'practice':
#                     student.lessons_balance -= 0.5 * count
#
#                 student.save()
#
#         # Проверяем удаленных студентов
#         for student in old_students:
#             count = 2 if form.cleaned_data.get(f'family_{student.pk}') else 1
#             if student not in new_students:
#                 if lesson.lesson_type == 'full':
#                     student.lessons_balance += 1 * count
#                 elif lesson.lesson_type == 'practice':
#                     student.lessons_balance += 0.5 * count
#
#                 student.save()
#     else:
#         students = form.cleaned_data.get('students')
#         for student in students:
#             count = 2 if form.cleaned_data.get(f'family_{student.pk}') else 1
#             if lesson.level == 'advanced':
#                 if lesson.lesson_type == 'full':
#                     student.lessons_balance -= 1 * count
#                 elif lesson.lesson_type == 'practice':
#                     student.lessons_balance -= 0.5 * count
#             elif lesson.level == 'beginner' and student.level == 'Начинающий':
#                 if lesson.lesson_type == 'full':
#                     student.lessons_balance -= 1 * count
#                 elif lesson.lesson_type == 'practice':
#                     student.lessons_balance -= 0.5 * count
#
#             student.save()
#
#     lesson.save()
#     form.save_m2m()
