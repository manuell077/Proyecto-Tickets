from django.shortcuts import render
from django.http import HttpResponse
from tickets.models import concept_low
from it_assets.models import device
from authenticathion.models import Division , Entity

def   manejoDeFormatos (request,form):
     


    if form == "BajaDeEquipo":
       
       usuario = request.user
       usuarioLogueado = Entity.objects.get(id = usuario.id)

       conceptos_de_baja = concept_low.objects.all() 
       
       subalternos = Division.objects.filter(parent_id = usuarioLogueado.division_id.id) 
 
       equipo = device.objects.filter(division_id__in = subalternos)

       contexto = {"Conceptos":conceptos_de_baja , "computadores": equipo}
       
       return render(request,"tickets/bajaDeEquipo.html",contexto)  
    
    elif form == "EntregaEquipo":
       
       return render(request,"tickets/bajaDeEquipo.html")  
       
   
           
    return HttpResponse("Formulario no encontrado" , Status=404)


