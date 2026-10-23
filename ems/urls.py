"""
URL configuration for ems project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from app01 import views

urlpatterns = [
    #部门管理
    path('admin/', admin.site.urls),
    path('depart/list/', views.depart_list1),
    path('depart/add/', views.depart_add1),
    path('depart/delete/', views.depart_delete1),
    path('depart/<int:nid>/edit/', views.depart_edit1),
    #用户管理
    path('user/list/', views.user_list),
    path('user/add/', views.user_add),
    path('user/model/form/add/', views.user_model_form_add),
    path('user/<int:nid>/edit/', views.user_edit),
    path('user/delete/', views.user_delete),
    #靓号管理
    path('pretty/list/', views.pretty_list),
    path('pretty/add/', views.pretty_add),
    path('pretty/delete/', views.pretty_delete),
    path('pretty/<int:nid>/edit/', views.pretty_edit),
]
