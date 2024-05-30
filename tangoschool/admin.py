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
    list_editable = ('level', 'is_active','phone_number')
    ordering = ('-is_active', '-level')
    search_fields = ('last_name',)
    list_filter = ("is_active", 'level')
    form = StudentForm

    def get_balance(self, obj):
        return obj.student_balance.balance

    def save_model(self, request, obj, form, change):
        initial_balance = form.cleaned_data.get('initial_balance')
        if not initial_balance:
            initial_balance = 0
        lesson_balance = form.cleaned_data.get('student_balance')
        if not lesson_balance:
            super().save_model(request, obj, form, change)

            if initial_balance > 0:
                Operation.objects.create(
                    operation_type='buying',
                    lesson_balance=obj.student_balance,
                    amount=initial_balance
                )
        elif lesson_balance and initial_balance > 0:
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


class OperationAdmin(admin.ModelAdmin):
    list_display = ('operation_type', 'student_name', 'amount', 'date', 'time')
    ordering = ('-date', '-time')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_type', 'lesson_topic', 'level', 'date', 'time')
    list_editable = ('lesson_topic', 'level')
    ordering = ('-date', '-time')
    filter_horizontal = ("students", 'guests')
    list_filter = ("lesson_type", 'level')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        students_before = set(obj.students.all())

        if 'students' in form.changed_data:
            students_after = set(form.cleaned_data['students'])
            added_students = students_after - students_before
            deleted_students = students_before - students_after

            # Добавление операций для новых студентов
            for student in added_students:
                if obj.lesson_type == 'practice':
                    amount = 0.5
                else:
                    amount = 1

                operation_date = obj.date
                operation_time = obj.time

                Operation.objects.create(
                    operation_type='visiting',
                    lesson_balance=student.student_balance,
                    amount=amount,
                    date=operation_date,
                    time=operation_time

                )

            # Удаление операций для удаленных студентов
            for student in deleted_students:
                start_datetime = datetime.combine(obj.date, obj.time) - timedelta(seconds=5)
                end_datetime = datetime.combine(obj.date, obj.time) + timedelta(seconds=5)
                operations = Operation.objects.filter(
                    lesson_balance=student.student_balance,
                    date=obj.date,
                    time__range=(start_datetime, end_datetime)
                )
                operations.delete()


admin.site.register(TrainerProfile, TrainerAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Guest)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Operation, OperationAdmin)


