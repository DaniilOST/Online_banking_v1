from django.urls import path
from . import views

app_name = 'online_banking'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('account/', views.account, name='account'),
    path('logout/', views.logout_view, name='logout'),
    path('create-account/', views.create_account, name='create_account'),
    path('transfer-funds/', views.transfer_funds, name='transfer_funds'),
]


