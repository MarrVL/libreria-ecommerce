from django.shortcuts import render, redirect, get_object_or_404
from .models import Libro, Carrito, ItemCarrito
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, 'pagCentral.html')

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def agregar_al_carrito(request, libro_id):
   libro = get_object_or_404(Libro, id=libro_id)

   # Busca o crea el carrito del usuario actual
   carrito, creado = Carrito.objects.get_or_create(usuario=request.user)

   # Obtener la cantidad del formulario
   cantidad = int(request.POST.get('cantidad', 1))

   # Busca si el libro ya está en el carrito
   item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, libro=libro)

   if not creado:
       # Si ya estaba, suma la nueva cantidad
       item.cantidad += cantidad
   else:
       # Si es nuevo, establece la cantidad
       item.cantidad = cantidad
   
   item.save()

   return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.select_related('libro')
    total = sum(item.subtotal() for item in items)

    return render(request, 'carrito/ver_carrito.html', {
        'carrito': carrito,
        'items': items,
        'total': total,
    })

@login_required
def eliminar_item(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.delete()
    return redirect('ver_carrito')

def libro_detail(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    return render(request, 'libros/libro_detail.html', {'libro': libro})

