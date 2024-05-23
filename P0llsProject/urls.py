from django.contrib import admin
from django.urls import path, include
from polls import views as polls_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('polls.urls')),
    path('login/', polls_views.user_login, name='login'),  # Use user_login here
    path('logout/', polls_views.user_logout, name='logout'),
]
