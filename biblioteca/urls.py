from django.urls import path
from . import views

urlpatterns = [
    path('', views.usuario_dashboard, name='usuario_dashboard'),

    # Libros
    path('libros/', views.LibroListView.as_view(), name='usuario_libro_list'),
    path('libros/nuevo/', views.LibroCreateView.as_view(), name='usuario_libro_create'),
    path('libros/<int:pk>/editar/', views.LibroUpdateView.as_view(), name='usuario_libro_update'),
    path('libros/<int:pk>/eliminar/', views.LibroDeleteView.as_view(), name='usuario_libro_delete'),
    path('exportar_libros_pdf/', views.exportar_libros_pdf, name='exportar_libros_pdf'),

    # Autores
    path('autores/', views.AutorListView.as_view(), name='usuario_autor_list'),
    path('autores/nuevo/', views.AutorCreateView.as_view(), name='usuario_autor_create'),
    path('autores/<int:pk>/editar/', views.AutorUpdateView.as_view(), name='usuario_autor_update'),
    path('autores/<int:pk>/eliminar/', views.AutorDeleteView.as_view(), name='usuario_autor_delete'),
    path('exportar_autores_pdf/', views.exportar_autores_pdf, name='exportar_autores_pdf'),

    # Préstamos
    path('prestamos/', views.PrestamoListView.as_view(), name='usuario_prestamo_list'),
    path('prestamos/nuevo/', views.PrestamoCreateView.as_view(), name='usuario_prestamo_create'),
    path('prestamos/<int:pk>/editar/', views.PrestamoUpdateView.as_view(), name='usuario_prestamo_update'),
    path('prestamos/<int:pk>/eliminar/', views.PrestamoDeleteView.as_view(), name='usuario_prestamo_delete'),
    path('exportar_prestamos_pdf/', views.exportar_prestamos_pdf, name='exportar_prestamos_pdf'),

    # Usuarios
    path('usuarios/', views.UsuarioListView.as_view(), name='usuario_usuario_list'),
    path('usuarios/nuevo/', views.UsuarioCreateView.as_view(), name='usuario_usuario_create'),
    path('usuarios/<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='usuario_usuario_update'),
    path('usuarios/<int:pk>/eliminar/', views.UsuarioDeleteView.as_view(), name='usuario_usuario_delete'),
    path('exportar_usuarios_pdf/', views.exportar_usuarios_pdf, name='exportar_usuarios_pdf'),
]
