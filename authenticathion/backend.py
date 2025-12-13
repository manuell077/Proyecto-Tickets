from django.contrib.auth.backends import BaseBackend #Importa la clase base que django utiliza para crear backends personalizados
from django.contrib.auth.hashers import check_password #Se importa una funcion que verifica si la contraseña en texto plano coincide con la contraseña hasheada 
from authenticathion.models import  Entity ,AccountUser #Modelo donde tenemos la cuenta de usuario
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import identify_hasher

def isPasswordHash(valor):
     try:
          identify_hasher(valor)
          return True
     except Exception:
          return False

class AutenthicathionDishospital(BaseBackend): #Esta nueva clase va a sobreescribir los metodos clave authenticate y get_user() 
      
    

      def authenticate(self,request,tipo_documento = None,numero_documento = None , password = None ): #Se personaliza la funcion authenticate ,  que recibe tres parametros el tipo de documento , numero documento y el password
          
          #Se hace un try except en el que se intenta buscar los datos en el modelo ENTITY
          try:
             principalUser = Entity.objects.get(identity_document_id = tipo_documento , document_number = numero_documento) #se busca en el modelo entity que es donde se tienen todos los datos los valores pasados como argumentos de la funcion authenticathe
             
          except Entity.DoesNotExist: #Si no encuentra los datos en el modelo entity
              
              return None
         
          userPassword = AccountUser.objects.get(entity_id = principalUser.id) #Busca la contraseña pero en el modelo accountUser que es donde se tienen las contraseñas 
          bd_hash = make_password(userPassword.password_hash) #Se hashea la contraseña la primera vez con make_password


          #Esta funcion va a entrar cuando el usuario se loguea por primera vez 
          if not isPasswordHash(userPassword.password_hash): #Aca se evalua con la funcion isPasswordHash que es para saber si la contraseña tiene algun tipo de hash mas no saber si esta hasheada como tal 
             print("La contraseña NO esta hasheada")
             userPassword.password_hash = bd_hash #Se guarda el valor  en el campo del modelo que es password_hash
             userPassword.save() #Se guarda en el modelo
         
           

          

          if check_password(password, userPassword.password_hash): #aca se evalua la contraseña si es igual a la que se paso como argumento en la funcion check_password
                print("Las contraseñas son iguales")
                return userPassword #Retorna el modelo del usuario 

          return None 
      
      def get_user(self,user_id):#Aca el get user se utiliza para devolver el modelo cada vez  que se hace un request.user 
            try:
                 return Entity.objects.get(pk=user_id) # Aca retorna el objeto
            
            except Entity.DoesNotExist: #retorna none si no encuentra nada 
                 
                 return None
                   