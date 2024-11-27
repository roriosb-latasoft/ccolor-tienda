from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Product, Transaccion
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm
from django.http import JsonResponse

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
    return render(request, 'pago.html')


def seguimiento(request):
    return render(request, 'seguimiento.html')


def exit(request):
    logout(request)
    return redirect('login')

def product_list(request):
    products = Product.objects.all()  # Obtén todos los productos de la base de datos
    return render(request, 'productos.html', {'products': products})


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



cart_data = []

def carrito(request):
    global cart_data
    if request.method == 'POST':
        import json
        cart_data = json.loads(request.body)
        return JsonResponse({'message': 'Carrito recibido correctamente'})

    # Renderizar la página de carrito con los datos actuales
    return render(request, 'carrito.html', {'cart_items': cart_data})


def pago(request):
    if request.method == 'GET':
        total = request.GET.get('total', '0.00')  # Desde la URL
    elif request.method == 'POST':
        total = request.POST.get('total', '0.00')  # Desde el formulario

    return render(request, 'pago.html', {'total': total})



from django.shortcuts import render, redirect
from django.http import JsonResponse
from .getnet_utils import crear_sesion_pago  # Asume que ya tienes esta función implementada

def procesar_pago(request):
    if request.method == "POST":
        total = request.POST.get("total")  # Captura el monto enviado desde carrito.html
        return render(request, "pago.html", {"total": total})
    return redirect("carrito")  # Redirige si el método no es POST

def iniciar_pago_getnet(request):
    if request.method == "POST":
        total = request.POST.get("total")  # Monto total
        referencia = "COMPRA-" + str(request.user.id)  # Genera una referencia única
        return_url = "ro.riosb.pythonanywhere.com/"  # Cambia según tu dominio

        # Llama a la función para crear la sesión en Getnet
        respuesta = crear_sesion_pago(referencia, total, return_url)
        
        if "processUrl" in respuesta:
            return redirect(respuesta["processUrl"])  # Redirige al Web Checkout de Getnet
        else:
            return JsonResponse({"error": respuesta.get("error", "Error al crear la sesión")})
    return redirect("carrito")  # Redirige si el método no es POST


def resultado_pago(request):
    estado = request.GET.get("status", "PENDIENTE")
    referencia = request.GET.get("reference", "SIN_REFERENCIA")
    
    if estado == "APPROVED":
        mensaje = "¡Pago aprobado!"
    elif estado == "REJECTED":
        mensaje = "El pago fue rechazado."
    else:
        mensaje = "El pago está pendiente de confirmación."

    return render(request, "resultado_pago.html", {"mensaje": mensaje, "referencia": referencia})
