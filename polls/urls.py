from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.user_login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.user_logout, name='logout'),
    path('polls/', views.poll_list, name='poll_list'),
    path('polls/<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('polls/<int:poll_id>/vote/', views.poll_vote, name='poll_vote'),
    path('polls/<int:poll_id>/results/', views.poll_results, name='poll_results'),
]
