from django.contrib import admin
from django.urls import path
from vulnerable_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('system-info/', views.system_info, name='system_info')
    path('logout/', views.user_logout, name='logout'),
    path('notes/', views.notes, name='notes'),
]