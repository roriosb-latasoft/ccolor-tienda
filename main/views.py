from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Product
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm
from django.http import JsonResponse
# importar dabases compras

# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def logros(request):
    return render(request, 'logros.html')

def contacto(request):
    return render(request, 'contacto.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def carrito(request):
    return render(request, 'carrito.html')

def pago(request):
    if request.method == 'POST':
        total = request.POST.get('total', '0.00')  # Recibe el total desde el formulario
    else:
        total = '0.00'  # Valor predeterminado si el método no es POST

    return render(request, 'pago.html', {'total': total})



def seguimiento(request):
    return render(request, 'seguimiento.html')


def exit(request):
    logout(request)
    return redirect('login')



def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Asunto del correo
            subject = "Nuevo Mensaje de Contacto"
            # Contenido del correo
            message = f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']} escribió:\n\n{form.cleaned_data['message']}"
            # Correo del remitente (quien envió el mensaje)
            sender = form.cleaned_data['email']
            # Tu correo de destino
            recipients = ['rodrigorios007@gmail.com']  # Cambia esto por tu correo

            try:
                send_mail(subject, message, sender, recipients)
                messages.success(request, "Tu mensaje ha sido enviado correctamente.")
                return redirect('contacto')
            except BadHeaderError:
                messages.error(request, "Se produjo un error al intentar enviar el correo.")
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = ContactForm()

    return render(request, 'contacto.html', {'form': form})



@login_required
def crud(request):
    products = Product.objects.all()  # Obtener todos los productos
    return render(request, 'crud.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            print("Datos válidos:", form.cleaned_data)  # Debug
            form.save()
            messages.success(request, 'Producto agregado exitosamente')
            return redirect('crud')
        else:
            print("Errores del formulario:", form.errors)  # Debug
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('crud')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Producto eliminado exitosamente')
    return redirect('crud')



from django.shortcuts import render, redirect
from django.http import JsonResponse
from transbank.webpay.webpay_plus.transaction import Transaction
from uuid import uuid4  # Para generar IDs únicos de compra


cart_data = []


def product_list(request):
    products = Product.objects.all()  # Obtén todos los productos de la base de datos
    return render(request, 'productos.html', {'products': products})


cart_data = []

def carrito(request):
    global cart_data
    if request.method == 'POST':
        import json
        cart_data = json.loads(request.body)
        return JsonResponse({'message': 'Carrito recibido correctamente'})

    # Renderizar la página de carrito con los datos actuales
    return render(request, 'carrito.html', {'cart_items': cart_data})
from django.shortcuts import render, redirect
from uuid import uuid4
from transbank.webpay.webpay_plus.transaction import Transaction


from uuid import uuid4
from datetime import datetime
from django.db import models


def iniciar_pago(request):
    total = request.GET.get("total", 0)  # Capturar el monto del carrito
    total = int(total)  # Convertir a entero

    data_post = request.POST

    print(data_post)

    url_retorno = request.build_absolute_uri('/confirmar_pago/')
    url_final = request.build_absolute_uri('/resultado_pago/')

    # insert data in compras
    
    print(request.GET)
    
    try:
        # Generar un identificador único y acortarlo
        session_id = str(uuid4())[:26]  # O usar datetime.now().strftime('%Y%m%d%H%M%S%f')[:26]

        respuesta = Transaction().create(
            buy_order = compra.id,
            session_id = session_id,
            amount = compra.total,
            return_url = url_retorno,
        )
        return redirect(respuesta['url'] + '?token_ws=' + respuesta['token'])
    except Exception as e:
        return render(request, 'error.html', {'mensaje': f"Error al iniciar el pago: {str(e)}"})


def confirmar_pago(request):
    # Obtener el token desde los parámetros GET
    token = request.GET.get("token_ws")

    if not token:
        return render(request, 'error.html', {'mensaje': "No se recibió un token válido desde Transbank."})

    try:
        # Confirmar la transacción con Webpay Plus
        respuesta = Transaction().commit(token)

        if respuesta['status'] == 'AUTHORIZED':
            # Si el pago es exitoso, generar un ID de compra único
            compra_id = str(uuid4())

            # Obtener datos del carrito y envío desde la sesión
            carrito = request.session.get('cart_data', [])
            envio = request.session.get('shipping_data', {})

            # Guardar la información de la compra en la sesión
            request.session['compra_exitosa'] = {
                'compra_id': compra_id,
                'carrito': carrito,
                'envio': envio,
                'total': respuesta['amount'],
            }

            return redirect('/resultado_pago/?success=true')
        else:
            return redirect('/resultado_pago/?success=false')
    except Exception as e:
        return render(request, 'error.html', {'mensaje': f"Error al procesar el pago: {str(e)}"})


def resultado_pago(request):
    # Verificar si el pago fue exitoso
    success = request.GET.get('success', 'false') == 'true'

    # Recuperar información de la compra desde la sesión
    compra_exitosa = request.session.pop('compra_exitosa', None)

    mensaje = "Pago realizado con éxito" if success else "Hubo un error en el pago"

    return render(request, 'resultado.html', {
        'mensaje': mensaje,
        'compra_exitosa': compra_exitosa,
        'success': success,
    })

from django.shortcuts import render

def carrito_view(request):
    # Obtén los productos del carrito desde la sesión
    cart_items = obtener_items_carrito(request)
    
    # Calcula el total asegurándote de que los valores son correctos
    total = sum(item['quantity'] * item['price'] for item in cart_items if item['price'] and item['quantity'])
    
    # Renderiza el template
    return render(request, 'carrito.html', {
        'cart_items': cart_items,
        'total': round(total, 2)  # Redondea a 2 decimales si es necesario
    })

def obtener_items_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    for item_id, detalles in carrito.items():
        # Asegúrate de que el precio y la cantidad sean números válidos
        price = float(detalles.get('price', 0))  # Convierte a float, predeterminado a 0 si está vacío
        quantity = int(detalles.get('quantity', 0))  # Convierte a entero
        items.append({
            'id': item_id,
            'name': detalles.get('name', 'Producto desconocido'),
            'price': price,
            'quantity': quantity,
        })
    return items

