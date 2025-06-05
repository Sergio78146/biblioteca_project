from django.test import TestCase
from biblioteca.models import Autor
from datetime import date

class AutorModelTest(TestCase):
    def test_creacion_autor(self):
        # Crear un autor con todos los campos
        autor = Autor.objects.create(
            nombre="Isabel",
            apellido="Allende",
            fecha_nacimiento=date(1942, 8, 2),
            nacionalidad="Chilena"
        )

        # Verificar que hay exactamente un autor en la base
        self.assertEqual(Autor.objects.count(), 1)

        # Recuperar el autor de la base de datos
        autor_db = Autor.objects.first()

        # Validar cada campo
        self.assertEqual(autor_db.nombre, "Isabel")
        self.assertEqual(autor_db.apellido, "Allende")
        self.assertEqual(autor_db.fecha_nacimiento, date(1942, 8, 2))
        self.assertEqual(autor_db.nacionalidad, "Chilena")

        # Validar el método __str__
        self.assertEqual(str(autor_db), "Isabel Allende")
