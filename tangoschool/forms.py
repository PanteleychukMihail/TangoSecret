from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import widgets
from datetime import date

from .models import *


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Користувач', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.TextInput(attrs={'class': 'form-input'}))


class AddStudentForm(forms.ModelForm):
    BALANCE_CHOICES = [
        ('new', 'Створити новий обліковий запис'),
        ('existing', 'Обрати існуючий')
    ]

    balance_choice = forms.ChoiceField(
        label='Тип облікового запису',
        choices=BALANCE_CHOICES,
        widget=forms.RadioSelect,
        initial='new'  # Установим по умолчанию выбор "Создать новую"
    )
    existing_balance = forms.ModelChoiceField(label='Тип облікового запису', queryset=Account.objects.all(),
                                              required=False,  # Делаем поле необязательным
                                              empty_label='Оберіть облиіковий запис')
    initial_balance = forms.IntegerField(required=False, label='Початковий баланс', initial=0)

    class Meta:
        model = Student
        exclude = ['student_balance']


class BuyLessonsForm(forms.Form):
    lessons = forms.FloatField(label='Кількість занять')


class AddLessonForm(forms.ModelForm):
    level = forms.ChoiceField(label='Рівень группы', choices=LEVEL_CHOICES, widget=forms.RadioSelect, required=True)
    students = forms.ModelMultipleChoiceField(
        label='Учні',
        queryset=Student.objects.filter(is_active=True).order_by('-level', '-last_name'),
        widget=forms.CheckboxSelectMultiple,
        required=False)
    date = forms.DateField(widget=forms.SelectDateWidget(), label='Дата')
    time = forms.TimeField(widget=forms.TimeInput(format='%H.%M'), label='Час')

    def __init__(self, *args, **kwargs):
        super(AddLessonForm, self).__init__(*args, **kwargs)
        self.fields['level'].initial = 'advanced'
        self.fields['lesson_type'].widget = forms.HiddenInput()
        self.fields['lesson_type'].initial = 'full'
        self.fields['date'].initial = date.today()

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
    time = forms.TimeField(widget=forms.TimeInput(format='%H.%M'), label='Час')

    guests = forms.ModelMultipleChoiceField(
        queryset=Guest.objects.all(), widget=forms.CheckboxSelectMultiple, required=False
    )

    def __init__(self, *args, **kwargs):
        super(AddPracticeForm, self).__init__(*args, **kwargs)
        self.fields['lesson_type'].widget = forms.HiddenInput()
        self.fields['lesson_type'].initial = 'practice'
        self.fields['date'].initial = date.today()

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
