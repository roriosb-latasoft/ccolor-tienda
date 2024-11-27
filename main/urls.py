from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [ 
    path('', views.index, name='index'),  
    path('logros/', views.logros, name='logros'),  
    path('nosotros/', views.nosotros, name='nosotros'),
    path('carrito/', views.carrito, name='carrito'),
    path('pago/', views.pago, name='pago'),
    path('crud/', views.crud, name='crud'),
    path('logout/', exit, name='exit'),
    path('productos/', views.product_list, name='product_list'),
    path('contacto/', views.contact_view, name='contacto'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.exit, name='exit'),
    path('seguimiento/', views.seguimiento, name='seguimiento'),
    path('carrito/pago/', views.procesar_pago, name='procesar_pago'),
    path('pago/getnet/', views.iniciar_pago_getnet, name='iniciar_pago_getnet'),
    path('pago/resultado/', views.resultado_pago, name='resultado_pago'),
    
    ]

