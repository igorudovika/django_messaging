from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views
from .views import HomeTemplateView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomeTemplateView.as_view(template_name='home.html'), name='home'),
    # API endpoints
    path('api/inbox/', views.inbox, name='inbox'),
    path('api/sent/', views.sent, name='sent'),
    path('api/inbox/<str:pk>/', views.message, name='message'),
    path('api/sent/<str:pk>/', views.message, name='message'),
    path('api/users/', views.users, name='users')
    ]
