"""
URL configuration for notee project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_document, name='upload_document'),
    path('document/<int:pk>/', views.document_detail, name='document_detail'),
    path('document/<int:pk>/edit/', views.edit_document, name='edit_document'),    
    path('note/new/', views.create_note, name='create_note'),
    path('note/<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('note/<int:note_id>/', views.note_detail, name='note_detail'),
    path('note/<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('document/<int:pk>/delete/', views.delete_document, name='delete_document'),
    path('auto-save-note/', views.auto_save_note, name='auto_save_note'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home, name='home'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

