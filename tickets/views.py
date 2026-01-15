from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from tickets.models import concept_low, tickets , low_team_format , equipment_delivery_format , request_tics , work_plan , response_data , area_request_tics , hadware_revision_format , authorizathion_hadware
from it_assets.models import device
from authenticathion.models import Division , Entity
from django.db.models import Q
from datetime import date

def   manejoDeFormatos (request,form,ticket_id=None):
     
    usuario = request.user #Se obtiene el usuario que realiza la request 
    usuarioLogueado = Entity.objects.get(id = usuario.id) #Se obtiene los datos de entity segun el usuario que realizo la solicitud
    Cargosubalternos = Division.objects.filter(parent_id = usuarioLogueado.division_id.id).values_list('id',flat=True) 
    subalternosId = Entity.objects.filter(division_id__in = Cargosubalternos)
    responsables = Entity.objects.filter(Q(id__in = subalternosId) | Q(id = usuario.id))
    responsable = Entity.objects.get(id = usuario.id )
    area = responsable.division_id.areas.name_area
    
    ticket = None
    modo = "crear"
    

    #Aca se verifica si llega por parametro el ticket_id 
    if ticket_id:
       ticket = get_object_or_404(tickets, id=ticket_id)
       modo = "editar"

    #Aca se valida si el metodo es post y no tiene un parametro entonces se crea el tricket por primera vez
    if request.method == "POST" and not ticket:
        titulo = request.POST.get("titulo")
        ticket = crear_ticket(titulo, usuario)
    
   
    formato = None
   #Aca se evalua que tipo de formato es para  renderizar el html que le pternece
    if form == "BajaDeEquipo":
       
       

       if ticket and modo == "editar":
          formato = low_team_format.objects.filter(ticket_id_id=ticket.id).first()


       if request.method == "POST":  #Si el request es post entonces vamos a obtener todos los datos que se envian por post 
          data  = {
             "description": request.POST.get('descripcion'),
                "authorized_siganture": request.POST.get('firma_baja'),
                "responsable_name": request.POST.get('realiza_baja'),
                "responsable_signature": request.POST.get('firma__responsable'),
                "date_format": request.POST.get('date'),
                "concept_low_id_id": request.POST.get('concepto_baja'),
                "device_id_id": request.POST.get('computador'),
                "header_id_id": 1,
                "ticket_id_id": ticket.id
          }
            
          if formato:
             for k , v in data.items():
                  setattr(formato,k,v)
             formato.save()
          else:
             low_team_format.objects.create(**data) 

             
         
      #  Trae todos los conceptos de baja para mostrar en el select 
       conceptos_de_baja = concept_low.objects.all() 
      #  Trae los subalternos del jefe ya que el jefe es el unico que va poder hacer los tickets
      # Se traen todos los equipos de los subalternos con Q es el operador OR de mysql entonces aqui nos va atraer si encuentra el entity_id de subalterno o del usuario que esta logueado o si encuenttra los dos los trae
       equipo = device.objects.filter(Q(entity_id__in = subalternosId) | Q(entity_id = usuario.id))
      # Aqui trae los datos de los subalternos 
       PropietariosComputadores = Entity.objects.filter(Q(id__in = subalternosId) | Q(id = usuario.id)).values_list('full_name',flat=True)
        
       EquipoNombre = zip(equipo , PropietariosComputadores)#Los mete en un  zip que es que mete dos listas o mas en pares. posicion por posicion  en este caso el de equipo y el propietario del equipo
       
       contexto = {"Conceptos":conceptos_de_baja ,  "UsuarioLogueo":usuarioLogueado , "EquipoNombre":EquipoNombre, "modo":modo , "formato":formato , "ticket":ticket } #Se le pasa todo el contexto 

       return render(request,"tickets/bajaDeEquipo.html",contexto)  #Renderizamos la vista de baja de Euipo
    
    elif form == "EntregaEquipo":
       
       if request.method == "POST":
          responsableNombre = request.POST.get('responsable')
          observaciones = request.POST.get('Observaciones')
          fechaPrestamo = request.POST.get('FechaPrestamo')
          fechaDevolucion = request.POST.get('fechaDevolucion')
          firmaRecibido = request.POST.get('Recibido_Por')
          firmarDevuelto = request.POST.get('firma_Devuelto')
         
          try : 
            
            equipment_delivery_format.objects.create(
             entity_id_id = responsableNombre,
             observations = observaciones,
             loan_date = fechaPrestamo,
             return_date = fechaDevolucion,
             received_siganture = firmaRecibido ,
             returned_signature = firmarDevuelto,
             header_id_id = 2,
             ticket_id_id = ticket.id
            )
            print("Se creo el formato bien")

          except Exception as e: 
             print("Ha ocurrido un error " , e)
          
       contexto = {"Dependencia":area, "Responsables":responsables}

       return render(request,"tickets/EntregaEquipo.html", contexto)  
       
      
    elif form == "SolicitudesTics":
        
        todosLosUsuarios = Entity.objects.all()
        
        if request.method == "POST":
           solicita = request.POST.get("Fechasolicita")
           tipoDeCambio = request.POST.get("tipoCambio")
           clase = request.POST.get("clase")
           Impacto = request.POST.get("Impacto")
           Prioridad = request.POST.get("prioridad")
           justificacion = request.POST.get("justificacionSolicitud")
           descripcionSolicitud = request.POST.get("descripcionSolicitud")
           areasSolicitud = request.POST.getlist("areas_solicitud[]")
           numero = request.POST.get("numero")
           actividad = request.POST.get("actividad")
           inicio = request.POST.get("inicio")
           final = request.POST.get("final")
           responsablePlan = request.POST.get("responsable")
           solicitudEstado = request.POST.get("solicitudEstado")
           descripcionDelRecuros = request.POST.get("descripcion")
           
           formatoSolicitud = request_tics.objects.create(
              impact = Impacto,
              class_new = clase,
              priority = Prioridad , 
              justification = justificacion , 
              description  = descripcionSolicitud , 
              header_id_id = 3 ,
              ticket_id_id = ticket.id,
              exchange_rate = tipoDeCambio,
              date_request = solicita
           )
        
           for  areas in areasSolicitud:
                print("El area es " , areas)
                area_request_tics.objects.create(
                    area_id_id = areas,
                    request_tics_id_id = formatoSolicitud.id
                )

           if(usuarioLogueado.division_id.id == 10):
             work_plan.objects.create(
              number_work_plan = numero,
              activity = actividad,
              resource_description = descripcionDelRecuros,
              start_work_plan = inicio ,
              end_work_plan = final ,
              entity_id_id = responsablePlan
             )

             response_data.objects.create(
              date_data = date.today(),
              request_tics_id_id = formatoSolicitud.id,
              user_id_id = usuarioLogueado.id,
              status_request = solicitudEstado
             )

        contexto = {"AreaSolicitante":area , "Encargado":usuarioLogueado.full_name , "Usuarios":todosLosUsuarios}

        return render(request,"tickets/SolicitudesTics.html",contexto) 
    elif form == "RevisionHadware":
         
         equipo = device.objects.filter(Q(entity_id__in = subalternosId) | Q(entity_id = usuario.id))
         PropietariosComputadores = Entity.objects.filter(Q(id__in = subalternosId) | Q(id = usuario.id)).values_list('full_name',flat=True)
         EquipoNombre = zip(equipo , PropietariosComputadores)#Los mete en un  zip que es que mete dos listas o mas en pares. posicion por posicion  en este caso el de equipo y el propietario del equipo
         
         

         if request.method == "POST":
            # Parte de formato 
            fecha_formato = request.POST.get("fechaSolicita")
            computadorRevisar = request.POST.get("computador")
            descripcionAnomalia = request.POST.get("anomaliaPresentada")
            revisadoPor = request.POST.get("revisadoPor")
            diagnosticar = request.POST.get("DiagnosticoRevision")
            soluciono = request.POST.get("soluciono")
            comprarNuevo = request.POST.get("comprarNuevo")
            comprarRepuestos = request.POST.get("comprarRepuestos")
            tiempoEstimado = request.POST.get("tiempoEstimado")
            
            #Parte de autorizacion
            fechaAutorizacion = request.POST.get("fechaAutorizacion")
            observacionesAutorizacion = request.POST.get("observaciones")
            firmaAutoriza = request.POST.get("firmaAutorizacion")
            areaAutorizacion = request.POST.get("areaAutorizacion")
            aprobarAutorizacion = request.POST.get("aprobado")
            
            hadware_format = hadware_revision_format.objects.create(
               date_format = fecha_formato,
               description = descripcionAnomalia,
               diagnostic = diagnosticar,
               solve = soluciono,
               buy_new = comprarNuevo,
               buy_spare_part = comprarRepuestos,
               estimated_time = tiempoEstimado,
               reviewed_internal_area = revisadoPor,
               device_id_id = computadorRevisar,
               header_id_id = 4,
               ticket_id_id = ticket.id
            ) 

             
            if(usuarioLogueado.division_id.id == 10):
               authorizathion_hadware.objects.create(
               hadware_format_id = hadware_format,
               date_authorizathion = fechaAutorizacion,
               authorizathion = aprobarAutorizacion,
               signature = firmaAutoriza,
               observation = observacionesAutorizacion,
               area_id_id = areaAutorizacion
               )

         contexto = {"AreaSolicitante":area, "Encargado":usuarioLogueado.full_name , "Equipos":EquipoNombre}
         return render(request,"tickets/RevisionHadware.html",contexto)      
     
    return HttpResponse("Formulario no encontrado" , status=404)


def crear_ticket(titulo, usuario):
    return tickets.objects.create(
        title=titulo,
        current_state='Pendiente',
        account_user_entity_id_id=usuario.id
    )