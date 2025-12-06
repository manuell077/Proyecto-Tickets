from django.urls import path 
from . import views


app_name = "core"

urlpatterns = [
    path('',views.base, name='menu'),
    path('submodulos/<int:module_id>/',views.get_submodules , name='submodules'),
    path('submodulos/contenido/<str:nombre_submodulo>/', views.cargarContenidoSubmodulos , name='contenido' )
]