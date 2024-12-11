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

from django.db import models

class Compras(models.Model):
    state = models.IntegerField(default=0) # boolean o str (3 estados: aceptado, rechazado, cancelado??)
    id_tbk = models.IntegerField(default=0)
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=15)
    telefono = models.CharField(max_length=12)
    correo = models.EmailField(max_length=100)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2) #
    direccion = models.CharField(max_length=300)
    neto = models.IntegerField(default=0) #
    iva = models.IntegerField(default=0) #
    total = models.IntegerField()  #
    date_time = models.DateTimeField(auto_now_add=True)
    
class produtosCompras(models.Model):
    id_compra = models.ForeignKey(Compras, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    oferta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_final = models.IntegerField()
    
class transbank(models.Model):
    id_compra = models.ForeignKey(Compras, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True) #
    session_id = models.CharField(max_length=100) # buscar 
    token_ws = models.CharField(max_length=200)
    # state = models.ForeignKey(Compras, on_delete=models.CASCADE) # Traer como FK o guardar acá?
    response_code = models.CharField(max_length=10, null=True, blank=True)
    orden_compra = models.IntegerField(max_length=100) #
    #faltan más datos para modelos