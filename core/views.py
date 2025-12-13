from django.shortcuts import render
from django.http import HttpResponse
from it_assets.models import device
from core.models import Entity_Permission_Submodule ,Submodule , Modulo , Permission
from authenticathion.models import Division ,Entity
from authenticathion.models import Entity
from django.http import JsonResponse
from django.template.loader import render_to_string



def base (request):
     
        usuario = request.user  #Trae el usuario que realiza la request 
           
        #Aca filtra y devulve un query set tryendo solo el valor de 'submodule_id'  sin repetir el mismo campo con distinct()    
        submodulos_ids = Entity_Permission_Submodule.objects.filter(entity_id=usuario.id).values_list('submodule_id', flat=True).distinct()
        #Aca filtra el modulo por el submodulo y que no se repita el mismo registro con distinct()
        modulos_ids = Submodule.objects.filter(id__in=submodulos_ids).values_list('module_id', flat=True).distinct()
        #Aca trae el modulo como tal del modelo 
        modulos = Modulo.objects.filter(id__in=modulos_ids)
        #Me trae los datos del usuario que esta logueado 
        usuarioLogueado = Entity.objects.get(id = usuario.id)

        #Aca en el  contexto se le pasan los datos del modulo el id del submodulo para que lo pase como parametro en la funcion del archivo estatico js , los datosDelUsuario que proviene tambien del modeloDeUsuarioLoguedo 
        contexto = {"modulos":modulos , "submodulos":submodulos_ids , "datosUser":usuarioLogueado , "Cargo":usuarioLogueado.division_id }
        

        return render(request,'core/base.html',contexto) #Renderiza el html con el contexto  en la url menu/
          
      
def get_submodules(request,module_id):


        Submodules = Submodule.objects.filter(module_id=module_id) #Hace un query set donde trae todos los submodulos  de acuerdo al modulo id 
        #recorre todos los submodulos de la base de datos remplaza el _  por un espcio en blanco y los vonvierte a mayusculas todo esto lo almacena en unJson
        data = {
                "submodules":[
                        {"id": s.id , "name": s.submodule_name.replace("_"," ").upper()}
                        for s in Submodules
                ]
        }

        return JsonResponse(data) # aca retorna el JsonResponse  con la informacion adentro en la url menu/submodulos

def cargarContenidoSubmodulos(request,nombre_submodulo):
        usuarioSolicitud = request.user

        nombreTemplate = nombre_submodulo.replace(" " , "_").lower() #aca se quita el espacio en blanco y se pone el "_" y se pasa a minusculas con el lower()
        usuariosPermiso = Entity_Permission_Submodule.objects.filter(entity_id = usuarioSolicitud.id).values_list('permission_id', flat=True)  
        permisos = Permission.objects.filter(id__in=usuariosPermiso)
        
        html = " "
        count = 0 
        permisoGuardado = " "
        for permiso in permisos:
          
          count += 1
          if permiso.permission_name != "create" and count == 1 :
             permisoGuardado = permiso.permission_name

          elif permisoGuardado != " ":
             direccion = f"tickets/{nombreTemplate}_{permisoGuardado}.html" #Aca se pone la url con el nombre del template que es lo mismo que el nombre del submodulo 
             html += render_to_string(direccion) #Se renderiza a string es decir el archivo se pasa a string

          else:
              direccion = f"tickets/{nombreTemplate}_{permiso.permission_name}.html" #Aca se pone la url con el nombre del template que es lo mismo que el nombre del submodulo 
              html += render_to_string(direccion) #Se renderiza a string es decir el archivo se pasa a string    
         
          
        return HttpResponse(html) #Este valor devuelve una respuesta httpResposne donde se le pone el html 

    #Esta vista esta asociada a la url submodulos/contenido 
     


