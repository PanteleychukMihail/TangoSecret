from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import *


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Пользователь', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.TextInput(attrs={'class': 'form-input'}))


class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class BuyLessonsForm(forms.Form):
    lessons = forms.IntegerField(label='Количество занятий')


class AddLessonForm(forms.ModelForm):
    level = forms.ChoiceField(choices=LEVEL_CHOICES, widget=forms.RadioSelect, required=True)
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.filter(is_active=True).order_by('level', 'user'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(AddLessonForm, self).__init__(*args, **kwargs)
        self.fields['level'].initial = 'advanced'

        for student in self.fields['students'].queryset:
            self.fields[f'family_{student.pk}'] = forms.BooleanField(
                label=f'Удвоение для {student}',
                required=False,
                widget=forms.CheckboxInput()
            )

    class Meta:
        model = Lesson
        fields = ['trainer', 'lesson_topic', 'lesson_type', 'level', 'students']


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
