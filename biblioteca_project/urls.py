from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from biblioteca import views as biblioteca_views  

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login personalizado
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),

    # Logout que redirige al login tras cerrar sesión
    path('accounts/logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    # Vista personalizada de registro
    path('accounts/registro/', biblioteca_views.registro, name='registro'),

    # URLs de la aplicación principal
    path('', include('biblioteca.urls')),
]
