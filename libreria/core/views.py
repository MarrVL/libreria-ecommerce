from django.shortcuts import render, redirect, get_object_or_404
from .models import Libro, Carrito, ItemCarrito, Categoria
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    categorias = Categoria.objects.all().order_by('nombre')
    libros_por_categoria = {}
    for categoria in categorias:
        libros_en_categoria = categoria.libros.all()
        libros_por_categoria[categoria.nombre] = libros_en_categoria
        print(f"Categoría: {categoria.nombre}, Libros encontrados: {libros_en_categoria.count()}")
        for libro in libros_en_categoria:
            print(f"  - {libro.titulo} (ID: {libro.id})")

    context = {
        'libros_por_categoria': libros_por_categoria,
        'categorias_disponibles': categorias,
    }
    return render(request, 'pagCentral.html', context)

def libros_por_categoria(request, categoria_slug):
    categoria = get_object_or_404(Categoria, nombre__iexact=categoria_slug.replace('-', ' ')) # Asume que el slug es el nombre normalizado
    libros = Libro.objects.filter(categoria=categoria)
    return render(request, 'libros/lista_categoria.html', {'categoria': categoria, 'libros': libros})

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

    # Busca si el libro ya está en el carrito
    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, libro=libro)

    if not creado:
        # Si ya estaba, incrementa la cantidad
        item.cantidad += 1
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

