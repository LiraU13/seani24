from django.urls import path

from . import views

app_name = 'exam'
urlpatterns = [
    path('', views.home, name='home'),
    path('module/<int:m_id>/questions/', views.question, name='question'),
    path('module/<int:m_id>/questions/<int:q_id>/', views.question, name='question'),
    path('create/', views.add_candidate, name='add_candidate'),
]