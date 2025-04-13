from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_question, name='add_question'),
    path('questions/', views.questions_list, name='questions_list'),
    path('quiz/', views.quiz, name='quiz'),
    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
]
