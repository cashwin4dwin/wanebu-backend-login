"""login_ms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from login_ms_app import login_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login2/v2/get-key',login_views.get_auth_key),
    path('login/v2/validate',login_views.verify_authkey),
    path('login/v2/', login_views.logedin_user_list),
    path('login/v2/<uuid:pk>',login_views.UsersLoginDetailedView.as_view()),
    path('login/v2/flow',login_views.UsersLoginListView.as_view()),
    path('login/v2/verify-sms', login_views.sms_verfication),
    path('login/v2/logout-user', login_views.logout_user),
]
