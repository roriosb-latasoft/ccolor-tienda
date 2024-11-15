from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Product
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm



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


@login_required
def crud(request):
    return render(request, 'crud.html')

def exit(request):
    logout(request)
    return redirect('index.html')

def product_list(request):
    products = Product.objects.all()  # Obtén todos los productos de la base de datos
    return render(request, 'productos.html', {'products': products})


from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from .forms import ContactForm

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


from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from django.contrib import messages

def crud(request):
    products = Product.objects.all()  # Obtener todos los productos
    return render(request, 'crud.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado exitosamente')
            return redirect('crud')
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



