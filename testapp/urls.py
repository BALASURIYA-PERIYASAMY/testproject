from django.contrib import admin
from django.urls import include, path
from .views import RegisterView, LoginView, CreateTestView, CreateQuestionView
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('create-test/', CreateTestView.as_view(), name='create-test'),
    path('create-question/', CreateQuestionView.as_view(), name='create-question'),
    path('',views.home, name='home'),
]
