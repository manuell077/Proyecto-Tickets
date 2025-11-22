from django.shortcuts import render
from authenticathion.models import IndentityDocument, AccountUser
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
#vista para login del sistema 
def loginDishospital(request):
    


    

    if request.method == "POST":
         tipo_documento = request.POST.get("tipo_documento")
         numero_documento = request.POST.get("numero_documento")
         password = request.POST.get("password")
         
         
        

         user = authenticate(
            request,
            tipo_documento = int(tipo_documento) ,
            numero_documento = numero_documento,
            password = password 
            )
         

         print("El usuario es " , user)

         if user is not None:
             # 1. OBTENER el AccountUser relacionado
            try:
                
                acc_user = AccountUser.objects.get(entity_id=user.entity_id)
                print("Obtuve el acc_user")
            except AccountUser.DoesNotExist:
                messages.error(request, "Usuario sin cuenta asociada")
                return redirect("login")
            
            
            # 2. GUARDAR EL entity_id PARA EL MIDDLEWARE
            request.session["entity_id"] = acc_user.entity_id
            

            # 3. LOGIN NORMAL DE DJANGO
            login(request, user)

            return redirect("tickets")
         
         else:
              messages.error(request,"Datos Incorrectos")


    lista_documentos = IndentityDocument.objects.all() #se hace una consulta con el modelo a la tabla en postgress para obtener todos los tipos de documentos Ejemplo "C.C:Cedula , T.I:Tarjeta de identidad"
    contexto = {'documentos_de_identidad':lista_documentos} #El contexto que se le va a pasar 
    return render(request,'authenticathion/index.html',contexto) #Se renderiza con el archivo html al que apúnta en este caso el index.html





