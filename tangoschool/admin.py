from django.contrib import admin
from .models import *


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'last_name', 'first_name', 'phone_number', 'email', 'birth_day', 'lessons_balance', 'level', 'is_active')
    list_editable = ('is_active',)


class TrainerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_first_name', 'user_last_name', 'phone_number', 'email', 'birth_day')
    list_select_related = ('user',)
    readonly_fields = ('user_first_name', 'user_last_name')

    def user_first_name(self, obj):
        return obj.user.first_name

    user_first_name.short_description = 'First name'

    def user_last_name(self, obj):
        return obj.user.last_name

    user_last_name.short_description = 'Last name'


class LessonAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        lesson = form.save(commit=False)

        if change:  # Проверяем, является ли это изменением существующего объекта
            old_lesson = Lesson.objects.get(pk=lesson.pk)  # Получаем старый объект урока

            if old_lesson.lesson_type != lesson.lesson_type:  # Проверяем изменение типа урока
                students = form.cleaned_data.get('students')

                for student in students:
                    if old_lesson.lesson_type == 'full':
                        student.lessons_balance += 0.5  # Возвращаем 0.5 к балансу, если предыдущий тип был 'full'

                    elif old_lesson.lesson_type == 'practice':
                        student.lessons_balance -= 0.5  # Возвращаем 1.0 к балансу, если предыдущий тип был 'practice'

                    student.save()

            old_students = old_lesson.students.all()
            new_students = form.cleaned_data['students']

            # Проверяем добавленных студентов
            for student in new_students:
                if student not in old_students:
                    if lesson.lesson_type == 'full':
                        student.lessons_balance -= 1
                    elif lesson.lesson_type == 'practice':
                        student.lessons_balance -= 0.5

                    student.save()

            # Проверяем удаленных студентов
            for student in old_students:
                if student not in new_students:
                    if lesson.lesson_type == 'full':
                        student.lessons_balance += 1
                    elif lesson.lesson_type == 'practice':
                        student.lessons_balance += 0.5

                    student.save()
        else:
            students = form.cleaned_data.get('students')
            for student in students:
                if lesson.lesson_type == 'full':
                    student.lessons_balance -= 1
                elif lesson.lesson_type == 'practice':
                    student.lessons_balance -= 0.5

                student.save()

        lesson.save()
        form.save_m2m()


admin.site.register(TrainerProfile, TrainerAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Guest)
admin.site.register(Lesson, LessonAdmin)
