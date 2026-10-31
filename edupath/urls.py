"""
URL configuration for edupath project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from assessment import views
import types

admin.site.login = views.signin
admin.site.logout = views.signout

# New admin users are created with is_superuser=True only (is_staff is hidden).
# Django's default has_permission only checks is_staff, so we extend it to also
# grant access to superusers — consistent with how the rest of the app treats them.
def _has_permission(self, request):
    return request.user.is_active and (request.user.is_staff or request.user.is_superuser)

admin.site.has_permission = types.MethodType(_has_permission, admin.site)

urlpatterns = [
    path('admin/logout/', views.signout, name='admin_logout'),
    path('admin/', admin.site.urls),
    path('', include('assessment.urls')),
]

