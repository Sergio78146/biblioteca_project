from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.models import Group

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import cm

from .models import Libro, Autor, Prestamo, Usuario
from django.contrib import messages



# Dashboard general
def usuario_dashboard(request):
    permisos = request.user.get_all_permissions()
    return render(request, 'usuario/dashboard.html', {'permisos': permisos})


# Registro
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            grupo = Group.objects.get(name='UsuarioComun')
            usuario.groups.add(grupo)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})


# LIBROS
class LibroListView(LoginRequiredMixin, ListView):
    model = Libro
    template_name = 'usuario/libro_list.html'

class LibroCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Libro
    fields = '__all__'
    template_name = 'usuario/libro_form.html'
    success_url = reverse_lazy('usuario_libro_list')
    permission_required = 'biblioteca.add_libro'

class LibroUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Libro
    fields = '__all__'
    template_name = 'usuario/libro_form.html'
    success_url = reverse_lazy('usuario_libro_list')
    permission_required = 'biblioteca.change_libro'

class LibroDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Libro
    template_name = 'usuario/libro_confirm_delete.html'
    success_url = reverse_lazy('usuario_libro_list')
    permission_required = 'biblioteca.delete_libro'


# AUTORES
class AutorListView(LoginRequiredMixin, ListView):
    model = Autor
    template_name = 'usuario/autor_list.html'

class AutorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Autor
    fields = '__all__'
    template_name = 'usuario/autor_form.html'
    success_url = reverse_lazy('usuario_autor_list')
    permission_required = 'biblioteca.add_autor'

class AutorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Autor
    fields = '__all__'
    template_name = 'usuario/autor_form.html'
    success_url = reverse_lazy('usuario_autor_list')
    permission_required = 'biblioteca.change_autor'

class AutorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Autor
    template_name = 'usuario/autor_confirm_delete.html'
    success_url = reverse_lazy('usuario_autor_list')
    permission_required = 'biblioteca.delete_autor'


# PRÉSTAMOS
class PrestamoListView(LoginRequiredMixin, ListView):
    model = Prestamo
    template_name = 'usuario/prestamo_list.html'


class PrestamoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Prestamo
    fields = '__all__'
    template_name = 'usuario/prestamo_form.html'
    success_url = reverse_lazy('usuario_prestamo_list')
    permission_required = 'biblioteca.add_prestamo'

    def form_valid(self, form):
        libro = form.cleaned_data['libro']
        if libro.cantidad_disponible > 0:
            libro.cantidad_disponible -= 1
            libro.save()
            return super().form_valid(form)
        else:
            form.add_error('libro', 'No hay ejemplares disponibles.')
            return self.form_invalid(form)



class PrestamoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Prestamo
    fields = '__all__'
    template_name = 'usuario/prestamo_form.html'
    success_url = reverse_lazy('usuario_prestamo_list')
    permission_required = 'biblioteca.change_prestamo'

    def form_valid(self, form):
        prestamo_anterior = self.get_object()
        prestamo_nuevo = form.save(commit=False)
        libro = prestamo_nuevo.libro

        # Si antes no estaba devuelto y ahora sí -> sumamos 1
        if not prestamo_anterior.devuelto and prestamo_nuevo.devuelto:
            libro.cantidad_disponible += 1
            libro.save()

        # Si antes estaba devuelto y ahora no -> restamos 1 (si hay disponibilidad)
        elif prestamo_anterior.devuelto and not prestamo_nuevo.devuelto:
            if libro.cantidad_disponible > 0:
                libro.cantidad_disponible -= 1
                libro.save()
            else:
                form.add_error('libro', 'No hay ejemplares disponibles para volver a prestar.')
                return self.form_invalid(form)

        return super().form_valid(form)



class PrestamoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Prestamo
    template_name = 'usuario/prestamo_confirm_delete.html'
    success_url = reverse_lazy('usuario_prestamo_list')
    permission_required = 'biblioteca.delete_prestamo'


# USUARIOS
class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuario/usuario_list.html'

class UsuarioCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Usuario
    fields = '__all__'
    template_name = 'usuario/usuario_form.html'
    success_url = reverse_lazy('usuario_usuario_list')
    permission_required = 'biblioteca.add_usuario'

class UsuarioUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Usuario
    fields = '__all__'
    template_name = 'usuario/usuario_form.html'
    success_url = reverse_lazy('usuario_usuario_list')
    permission_required = 'biblioteca.change_usuario'

class UsuarioDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'usuario/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario_usuario_list')
    permission_required = 'biblioteca.delete_usuario'


# EXPORTACIONES A PDF

def exportar_autores_pdf(request):
    if not request.user.has_perm('biblioteca.view_autor'):
        return HttpResponse("No tienes permiso para exportar.", status=403)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="autores.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, "Listado de Autores")
    p.setFont("Helvetica", 12)

    autores = Autor.objects.all().values_list('nombre', 'apellido', 'fecha_nacimiento')
    data = [["Nombre", "Apellido", "Fecha de nacimiento"]]
    for nombre, apellido, fecha in autores:
        data.append([nombre, apellido, fecha.strftime('%d/%m/%Y')])

    table = Table(data, colWidths=[6*cm, 6*cm, 5*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4B8BBE")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
    ]))
    table.wrapOn(p, width, height)
    table.drawOn(p, 40, height - 100 - len(data)*15)
    p.showPage()
    p.save()
    return response


def exportar_libros_pdf(request):
    if not request.user.has_perm('biblioteca.view_libro'):
        return HttpResponse("No tienes permiso para exportar.", status=403)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="libros.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, "Listado de Libros")
    p.setFont("Helvetica", 12)

    libros = Libro.objects.all().values_list('titulo', 'autor__nombre', 'autor__apellido', 'anio_publicacion')
    data = [["Título", "Autor", "Año"]]
    for titulo, nombre, apellido, anio in libros:
        data.append([titulo, f"{nombre} {apellido}", str(anio)])

    table = Table(data, colWidths=[8*cm, 6*cm, 2*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4B8BBE")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
    ]))
    table.wrapOn(p, width, height)
    table.drawOn(p, 40, height - 100 - len(data)*15)
    p.showPage()
    p.save()
    return response

def exportar_prestamos_pdf(request):
    if not request.user.has_perm('biblioteca.view_prestamo'):
        return HttpResponse("No tienes permiso para exportar.", status=403)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="prestamos.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, "Listado de Préstamos")
    p.setFont("Helvetica", 12)

    prestamos = Prestamo.objects.select_related('usuario', 'libro').all()

    data = [["Usuario", "Libro", "Fecha Préstamo", "Fecha Devolución", "Devuelto"]]

    for prestamo in prestamos:
        usuario = f"{prestamo.usuario.nombre} {prestamo.usuario.apellido}"
        libro = prestamo.libro.titulo
        fecha_prestamo = prestamo.fecha_prestamo.strftime('%d/%m/%Y')
        fecha_devolucion = prestamo.fecha_devolucion.strftime('%d/%m/%Y') if prestamo.fecha_devolucion else "Pendiente"
        devuelto = "Sí" if prestamo.devuelto else "No"
        data.append([usuario, libro, fecha_prestamo, fecha_devolucion, devuelto])

    table = Table(data, colWidths=[5*cm, 5*cm, 3*cm, 3*cm, 2*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4B8BBE")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
    ]))

    table.wrapOn(p, width, height)
    table.drawOn(p, 40, height - 100 - len(data) * 18)

    p.showPage()
    p.save()
    return response

def exportar_usuarios_pdf(request):
    if not request.user.has_perm('biblioteca.view_usuario'):
        return HttpResponse("No tienes permiso para exportar.", status=403)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="usuarios.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, "Listado de Usuarios")
    p.setFont("Helvetica", 12)

    usuarios = Usuario.objects.all().values_list('nombre', 'apellido', 'email', 'telefono', 'direccion')
    data = [["Nombre", "Apellido", "Email", "Teléfono", "Dirección"]]
    for usuario in usuarios:
        data.append(list(usuario))

    # Ajuste proporcional del ancho total disponible
    table_width = width - 80  # Deja 40px de margen a izquierda y derecha
    colWidths = [0.15, 0.15, 0.3, 0.15, 0.25]  # proporción relativa
    colWidths = [table_width * w for w in colWidths]

    table = Table(data, colWidths=colWidths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4B8BBE")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    table.wrapOn(p, width, height)
    table_height = len(data) * 18
    table.drawOn(p, 40, height - 100 - table_height)

    p.showPage()
    p.save()
    return response