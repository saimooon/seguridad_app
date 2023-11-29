# En urls.py
from django.urls import path
from registro.views import signup, home, user_login, manage_messages
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('manage_messages/<int:message_id>/', manage_messages, name='manage_messages'),
]
