from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logout, name='logout'),
    path('field_study/', views.field_study, name='field_study'),
    path('about/', views.about, name='about'),
    path('cs/', views.cs, name='cs'),
    path('telecom/', views.telecom, name='telecom'),
    path('edusci/', views.edusci, name='edusci'),
    path('eduart/', views.eduart, name='eduart'),
    path('industrial/', views.industrial, name='industrial'),
    path('nursing/', views.nursing, name='nursing'),
    path('contact/', views.contact, name='contact'),
    path('mentor/', views.mentor, name='mentor'),
    path('programming_in_c_quiz/', views.programming_in_c_quiz, name='programming_in_c_quiz'),
    path('programming-in-c-quiz-results/', views.programming_in_c_quiz_results, name='programming_in_c_quiz_results'),
    path('java_quiz/', views.java_quiz, name='java_quiz'),
    path('java_quiz_results/', views.java_quiz_results, name='java_quiz_results'),
    path('software_engineering_quiz/', views.software_engineering_quiz, name='software_engineering_quiz'),
    path('software_engineering_quiz_results/', views.software_engineering_quiz_results, name='software_engineering_quiz_results'),
    path('login1/', views.login1, name='login1'),
    path('lec/<int:course_id>/', views.lec, name='lec'),
    path('score/<int:course_id>/', views.score_view, name='score'),
]
