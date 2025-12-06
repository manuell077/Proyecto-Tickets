from django.shortcuts import render
from django.http import HttpResponse
from core.models import Entity_Permission_Submodule ,Submodule , Modulo 
from authenticathion.models import Division ,Entity
from authenticathion.models import Entity
from django.http import JsonResponse
from django.template.loader import render_to_string



def base (request):
     
        usuario = request.user

        submodulos_ids = Entity_Permission_Submodule.objects.filter(entity_id=usuario.id).values_list('submodule_id', flat=True).distinct()

        modulos_ids = Submodule.objects.filter(id__in=submodulos_ids).values_list('module_id', flat=True).distinct()

        modulos = Modulo.objects.filter(id__in=modulos_ids)
        
        usuarioLogueado = Entity.objects.get(id = usuario.id)
        

        


        contexto = {"modulos":modulos , "submodulos":submodulos_ids , "datosUser":usuarioLogueado , "Cargo":usuarioLogueado.division_id}
        

        return render(request,'core/base.html',contexto)
          
      


def get_submodules(request,module_id):


        Submodules = Submodule.objects.filter(module_id=module_id)

        data = {
                "submodules":[
                        {"id": s.id , "name": s.submodule_name.replace("_"," ").upper()}
                        for s in Submodules
                ]
        }

        return JsonResponse(data)

def cargarContenidoSubmodulos(request,nombre_submodulo):
     
        nombreTemplate = nombre_submodulo.replace(" " , "_").lower()
        

        direccion = f"tickets/{nombreTemplate}.html"
        
        

        html = render_to_string(direccion)

        return HttpResponse(html)
     



