from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginUserForm, AddStudentForm, AddLessonForm, BuyLessonsForm, AddPracticeForm
from .utils import *


class SchoolHome(DataMixin, TemplateView):
    template_name = 'tangoschool/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Танго Сикрет")
        return dict(list(context.items()) + list(c_def.items()))


class AddStudent(LoginRequiredMixin, DataMixin, CreateView):
    model = Student
    form_class = AddStudentForm
    template_name = 'tangoschool/student_add.html'
    success_url = reverse_lazy('users_list')

    def form_valid(self, form):
        balance_choice = form.cleaned_data.get('balance_choice')
        initial_balance = form.cleaned_data.get('initial_balance')

        if balance_choice == 'new':
            balance = Account.objects.create()
            if initial_balance:
                Operation.objects.create(
                    operation_type='buying',
                    lesson_balance=balance,
                    amount=initial_balance
                )

        else:
            existing_balance = form.cleaned_data.get('existing_balance').id
            balance = Account.objects.get(id=existing_balance)
            if initial_balance:
                Operation.objects.create(
                    operation_type='buying',
                    lesson_balance=balance,
                    amount=initial_balance
                )

        form.instance.student_balance = balance
        return super().form_valid(form)

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Додати учня")
        return dict(list(context.items()) + list(c_def.items()))


class StudentsList(LoginRequiredMixin, DataMixin, ListView):
    model = Student
    template_name = 'tangoschool/students_list.html'
    context_object_name = 'students'
    login_url = reverse_lazy('home')

    def get_queryset(self):
        # Фильтруем учеников, у которых is_active=True
        return Student.objects.filter(is_active=True)

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Список учнів")
        return dict(list(context.items()) + list(c_def.items()))


class ShowStudent(LoginRequiredMixin, DataMixin, DetailView):
    model = Student
    template_name = "tangoschool/student_show.html"
    context_object_name = 'student'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Информація про учня")
        student = self.get_object()
        operations = student.student_balance.operations.all().order_by('-date', '-time')
        balance = student.student_balance
        balance_value = balance.balance
        context['balance'] = balance_value
        context['operations'] = operations
        return dict(list(context.items()) + list(c_def.items()))


class BuyLessonsView(DataMixin, View):
    template_name = 'tangoschool/buy_lessons.html'
    form_class = BuyLessonsForm

    def get(self, request, pk):
        student = Student.objects.get(pk=pk)
        context = {
            'title': f'Купівля занять для учня {student}',
            'form': self.form_class()
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        student = Student.objects.get(pk=pk)
        balance = student.student_balance
        form = self.form_class(request.POST)
        if form.is_valid():
            lessons = form.cleaned_data['lessons']
            if balance:
                Operation.objects.create(
                    operation_type='buying',
                    lesson_balance=balance,
                    amount=lessons
                )
                balance.save()
        else:
            existing_balance = form.cleaned_data.get('existing_balance').id
            Account.objects.get(id=existing_balance)
        return redirect('student', pk=pk)


class LessonCreateView(LoginRequiredMixin, DataMixin, CreateView):
    model = Lesson
    form_class = AddLessonForm
    template_name = 'tangoschool/lesson_create.html'
    success_url = reverse_lazy('lessons_view')

    def form_valid(self, form):
        lesson = form.save(commit=False)
        lesson.trainer1 = form.cleaned_data.get('trainer1')
        lesson.trainer2 = form.cleaned_data.get('trainer2')
        students = form.cleaned_data.get('students')
        lesson_level = form.cleaned_data.get('level')
        lesson.date = form.cleaned_data.get('date')
        lesson.time = form.cleaned_data.get('time')

        for student in students:
            balance = student.student_balance
            operation = Operation.objects.create(
                operation_type='visiting',
                lesson_balance=student.student_balance,
                amount=1,
                date=lesson.date,
                time=lesson.time
            )
            balance.save()
        create_and_send_excel_report()
        return super().form_valid(form)

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Додати заняття")
        return dict(list(context.items()) + list(c_def.items()))


class PracticeCreateView(LoginRequiredMixin, DataMixin, CreateView):
    model = Lesson
    form_class = AddPracticeForm
    template_name = 'tangoschool/practice_create.html'
    success_url = reverse_lazy('lessons_view')

    def form_valid(self, form):
        lesson = form.save(commit=False)
        students = form.cleaned_data.get('students')
        guests = form.cleaned_data.get('guests')
        guests_total_money = len(guests) * 100

        for student in students:
            balance = student.student_balance
            operation = Operation.objects.create(
                operation_type='visiting',
                lesson_balance=student.student_balance,
                amount=0.5,
                date=lesson.date,
                time=lesson.time

            )
            balance.save()
        lesson.guests_total_money = guests_total_money
        create_and_send_excel_report()
        return super().form_valid(form)

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Додати практику")
        return dict(list(context.items()) + list(c_def.items()))


class LessonsViews(LoginRequiredMixin, DataMixin, ListView):
    model = Lesson
    template_name = 'tangoschool/lessons.html'
    context_object_name = 'lessons'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Список занять")
        return dict(list(context.items()) + list(c_def.items()))


class LessonShow(LoginRequiredMixin, DataMixin, DetailView):
    model = Lesson
    template_name = "tangoschool/lesson_show.html"
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()
        students = lesson.students.all()
        guests = lesson.guests.all()
        context['students'] = students
        context['guests'] = guests
        c_def = self.get_user_context(title="Информаці про урок")
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'tangoschool/login.html'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизація")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена </h1>')

# class StudentUpdate(LoginRequiredMixin, DataMixin, DetailView):
#     model = User#
#     form_class = UpdateUserForm
#     template_name = 'tangoschool/student_update.html'
#     success_url = reverse_lazy('home')
#     pk_url_kwarg = 'slug'
