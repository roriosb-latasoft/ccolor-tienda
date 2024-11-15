from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre del Producto")
    type = models.CharField(max_length=100, verbose_name="Tipo de Producto")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Imagen del Producto")
    stock = models.PositiveIntegerField(default=0, verbose_name="Cantidad en Inventario")
    description = models.TextField(null=True, blank=True, verbose_name="Descripción del Producto")

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
