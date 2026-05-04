from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.start_test, name='start_test'),
    path('submit/', views.submit_test, name='submit_test'),
    path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),
path('signup/', views.signup_view, name='signup'),
path('dashboard/', views.dashboard, name='dashboard'),
path('profile/', views.profile_view, name='profile'),
path('profile/edit/', views.edit_profile, name='edit_profile'),
path('result/<int:id>/', views.view_result, name='view_result'),
# urls.py
path('delete-result/<int:id>/', views.delete_result, name='delete_result'),
]
