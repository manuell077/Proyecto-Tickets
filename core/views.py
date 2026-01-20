from django.shortcuts import render
from django.http import HttpResponse
from it_assets.models import device
from core.models import Entity_Permission_Submodule ,Submodule , Modulo , Permission
from authenticathion.models import Division ,Entity
from tickets.models import tickets
from authenticathion.models import Entity
from django.http import JsonResponse
from django.template.loader import render_to_string
from core.submodulos import SUBMODULOS



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
        ModuloNombre = Modulo.objects.get(id = module_id).module_name #Me trae el nombre del modulo

        #recorre todos los submodulos de la base de datos remplaza el _  por un espcio en blanco y los vonvierte a mayusculas todo esto lo almacena en unJson
        data = {
                "submodules":[
                        {"id": s.id , "name": s.submodule_name.replace("_"," ").upper(),"nombreModulo":ModuloNombre}
                        for s in Submodules
                ]
        }

        return JsonResponse(data) # aca retorna el JsonResponse  con la informacion adentro en la url menu/submodulos

def cargarContenidoSubmodulos(request,nombre_submodulo,nombre_modulo):
        usuarioSolicitud = request.user
        
        nombreDelModuloMinusculas = nombre_modulo.lower()
        nombreTemplate = nombre_submodulo.replace(" " , "_").lower() #aca se quita el espacio en blanco y se pone el "_" y se pasa a minusculas con el lower()
        usuariosPermiso = Entity_Permission_Submodule.objects.filter(entity_id = usuarioSolicitud.id).values_list('permission_id', flat=True)  
        permisos = set(Permission.objects.filter(id__in=usuariosPermiso).values_list("permission_name",flat=True))
        
        direccion = ""
        html = ""
        if "create" in permisos:
           direccion = f"{nombre_modulo}/{nombreTemplate}_create.html"
           html += render_to_string(direccion)     
        if "view" in permisos:
           
           config = SUBMODULOS.get(nombreTemplate) 

           ticketsUsuario = config['queryset'](usuarioSolicitud) 
           FORMATOS = config.get('formatos',{})
           
           tickets_con_formato = [] #Se crea una lista para guardar por cada ticket su informacion 

           for ticket in ticketsUsuario: #Se recorren los tickets que nos trajo el query set  
               
               for attr, conf in FORMATOS.items():#Ahora se recorren el dicccionario de los formatos item por item   
                  if hasattr(ticket, attr):#buscando en cada objeto ticket que se recorre en el querySet el atributo que es la clave del diccionario
                     formato = conf['nombre'] #En la variable de formato guardamos el nombre que es el valor que almacena la clave
                     fecha = conf['fecha'](ticket)
                     observacion = conf['observacion'](ticket)
                     break

               formato_en_mayusculas_pegado = ''.join(p.capitalize() for p in formato.lower().split())
               
        
               tickets_con_formato.append({ #En la lista lo vamos añadiendo 
               'ticket': ticket,
               'formato_mayusculas':formato_en_mayusculas_pegado,
               'formato': formato,
               'fecha' : fecha,
               'observacion': observacion,
               'estado' : ticket.current_state
                })            
            
           contexto = {"tickets":tickets_con_formato , "nombreModulo":nombreDelModuloMinusculas } #Y en el contexto le pasamos la lista  por cada ticket su formato 
           direccion = f"{nombre_modulo}/{nombreTemplate}_view.html"
           html += render_to_string(direccion, contexto)      
          
        return HttpResponse(html) #Este valor devuelve una respuesta httpResposne donde se le pone el html 

    #Esta vista esta asociada a la url submodulos/contenido 
     