#la_pontificia_horarios/urls.py
"""
URL configuration for la_pontificia_horarios project.

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
# la_pontificia_horarios/urls.py (Versión corregida y limpia)
from django.contrib import admin
from django.urls import path, include
from apps.users.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Endpoints de autenticación (JWT)
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Incluir URLs de tus aplicaciones
    # Este es el CAMBIO CLAVE
    path('api/academic-setup/', include('apps.academic_setup.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/scheduling/', include('apps.scheduling.urls')),
]