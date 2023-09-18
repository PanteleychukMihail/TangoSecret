from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets
from datetime import date

from .models import *


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Пользователь', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.TextInput(attrs={'class': 'form-input'}))


class AddStudentForm(forms.ModelForm):
    balance_choice = forms.ChoiceField(label='Тип учетной записи',
                                       choices=[('new', 'Создать новую учетную запись'),
                                                ('existing', 'Выбрать существующую')],
                                       widget=forms.RadioSelect  # Используем радиокнопки для выбора
                                       )
    existing_balance = forms.ModelChoiceField(label='Тип учетной записи', queryset=Account.objects.all(),
                                              required=False,  # Делаем поле необязательным
                                              empty_label='Выберите учетную запись')
    initial_balance = forms.IntegerField(required=False, label='Начальный баланс', initial=0)

    class Meta:
        model = Student
        exclude = ['student_balance']


class BuyLessonsForm(forms.Form):
    lessons = forms.IntegerField(label='Количество занятий')


class AddLessonForm(forms.ModelForm):
    level = forms.ChoiceField(label='Уровень группы', choices=LEVEL_CHOICES, widget=forms.RadioSelect, required=True)
    students = forms.ModelMultipleChoiceField(
        label='Ученики',
        queryset=Student.objects.filter(is_active=True).order_by('-level', '-last_name'),
        widget=forms.CheckboxSelectMultiple,
        required=False)
    date = forms.DateField(widget=widgets.SelectDateWidget(), label='Дата',initial=date.today())
    time = forms.TimeField(widget=forms.TimeInput(format='%H.%M'), label='Время')

    def __init__(self, *args, **kwargs):
        super(AddLessonForm, self).__init__(*args, **kwargs)
        self.fields['level'].initial = 'advanced'
        self.fields['lesson_type'].widget = forms.HiddenInput()
        self.fields['lesson_type'].initial = 'full'

    class Meta:
        model = Lesson
        fields = ['date', 'time','lesson_type', 'lesson_topic', 'trainer1', 'trainer2', 'level', 'students']


class AddPracticeForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.filter(is_active=True).order_by('level', 'last_name'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    date = forms.DateField(widget=widgets.SelectDateWidget(), label='Дата',initial=date.today())
    time = forms.TimeField(widget=forms.TimeInput(format='%H.%M'), label='Время')

    guests = forms.ModelMultipleChoiceField(
        queryset=Guest.objects.all(), widget=forms.CheckboxSelectMultiple, required=False
    )

    def __init__(self, *args, **kwargs):
        super(AddPracticeForm, self).__init__(*args, **kwargs)
        self.fields['lesson_type'].widget = forms.HiddenInput()
        self.fields['lesson_type'].initial = 'practice'

    class Meta:
        model = Lesson
        fields = ['date', 'time', 'lesson_type', 'students', 'guests']

# class UpdateUserForm(forms.ModelForm):
#     model = User
#     fields = ('email', 'password', 'phone_number', 'birth_day','photo')
#
#
# class RegisterUserForm(UserCreationForm):
#     username = forms.CharField(label='логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
#     email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
#     password1 = forms.CharField(label='пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
#     password2 = forms.CharField(label='повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',)
