from django.urls import path
from .views import *

urlpatterns = [
    path('', SchoolHome.as_view(), name='home'),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', logout_user, name="logout"),
    path('add_student/', AddStudent.as_view(), name='add_student'),
    path('students/', StudentsList.as_view(), name='users_list'),
    path('student/<str:pk>/', ShowStudent.as_view(), name='student'),
    path('student/<str:pk>/buy_lessons/', BuyLessonsView.as_view(), name='buy_lessons'),
    path('add_lesson/', LessonCreateView.as_view(), name='add_lesson'),
    path('add_practice', PracticeCreateView.as_view(), name='add_practice'),
    path('lessons_view/', LessonsViews.as_view(), name='lessons_view'),
    path('lesson_view/<str:pk>/', LessonShow.as_view(), name='lesson'),
    # path('register/', RegisterUser.as_view(), name="register"),
    # path('student_update/', StudentUpdate.as_view(), name='user_update'),

]




