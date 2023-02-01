from django.urls import path

from chat import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('chat/<str:room_name>/', views.room),
]