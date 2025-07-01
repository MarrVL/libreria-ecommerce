from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<str:libro_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_item, name='eliminar_item'),
    path('libros/<str:libro_id>/', views.libro_detail, name='libro_detail'),
    path('libros/categoria/<str:categoria_slug>/', views.libros_por_categoria, name='nombre_de_tu_vista_para_categoria'),
]
            