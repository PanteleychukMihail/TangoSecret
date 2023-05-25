from datetime import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View, generic
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginUserForm, AddStudentForm, AddLessonForm, BuyLessonsForm
from .models import *
from .utils import *


class SchoolHome(DataMixin, TemplateView):
    template_name = 'tangoschool/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Танго Сикрет")
        return dict(list(context.items()) + list(c_def.items()))


class AddStudent(LoginRequiredMixin, DataMixin, CreateView):
    model = User
    form_class = AddStudentForm
    template_name = 'tangoschool/student_add.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить студента")
        return dict(list(context.items()) + list(c_def.items()))


class StudentsList(LoginRequiredMixin, DataMixin, ListView):
    model = Student
    template_name = 'tangoschool/students_list.html'
    context_object_name = 'students'
    login_url = reverse_lazy('home')

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Список Студентов")
        return dict(list(context.items()) + list(c_def.items()))


class ShowStudent(LoginRequiredMixin, DataMixin, DetailView):
    model = Student
    template_name = "tangoschool/student_show.html"
    context_object_name = 'student'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Информация о студенте")
        return dict(list(context.items()) + list(c_def.items()))


class BuyLessonsView(DataMixin, View):
    template_name = 'tangoschool/buy_lessons.html'
    form_class = BuyLessonsForm

    def get(self, request, pk):
        student = Student.objects.get(pk=pk)
        context = {
            'title': f'Покупка занятий для ученика {student}',
            'form': self.form_class()
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        student = Student.objects.get(pk=pk)
        form = self.form_class(request.POST)
        if form.is_valid():
            lessons = form.cleaned_data['lessons']
            student.lessons_balance += lessons
            student.save()
            return redirect('student', pk=pk)
        else:
            context = {
                'title': f'Покупка занятий для ученика {student}',
                'form': form
            }
            return render(request, self.template_name, context)


# class StudentUpdate(LoginRequiredMixin, DataMixin, DetailView):
#     model = User
#
#     form_class = UpdateUserForm
#     template_name = 'tangoschool/student_update.html'
#     success_url = reverse_lazy('home')
#     pk_url_kwarg = 'slug'

class LessonCreateView(LoginRequiredMixin, DataMixin, CreateView):
    model = Lesson
    form_class = AddLessonForm
    template_name = 'tangoschool/lesson_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        lesson = form.save()
        lesson.trainer = form.cleaned_data.get('trainer')
        students = form.cleaned_data.get('students')

        for student in students:
            count = 1
            family_key = f'family_{student.pk}'
            is_family = self.request.POST.get(family_key) == 'on'

            if is_family:
                count *= 2  # Multiply the count by 2 for students with family checkbox checked

            if lesson.lesson_type == 'full':
                student.lessons_balance -= 1 * count
            elif lesson.lesson_type == 'practice':
                student.lessons_balance -= 0.5 * count

            student.save()

        lesson.save()
        return redirect('home')

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить занятие")
        return dict(list(context.items()) + list(c_def.items()))


class LessonsViews(DataMixin, ListView):
    model = Lesson
    template_name = 'tangoschool/lessons.html'
    context_object_name = 'lessons'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Список занятий")
        return dict(list(context.items()) + list(c_def.items()))


class LessonShow(LoginRequiredMixin, DataMixin, DetailView):
    model = Lesson
    template_name = "tangoschool/lesson_show.html"
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()
        students = lesson.students.all()
        print(students)
        context['students'] = students
        c_def = self.get_user_context(title="Информация об уроке")
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'tangoschool/login.html'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


# class RegisterUser(DataMixin, CreateView):
#     form_class = RegisterUserForm
#     template_name = 'tangoschool/student_update.html'
#     success_url = reverse_lazy('login')
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('home')
#
#     def get_context_data(self, *, objects_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Регистрация")
#         return dict(list(context.items()) + list(c_def.items()))


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена </h1>')
