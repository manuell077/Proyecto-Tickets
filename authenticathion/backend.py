from django.contrib.auth.backends import BaseBackend #Importa la clase base que django utiliza para crear backends personalizados
from django.contrib.auth.hashers import check_password #Se importa una funcion que verifica si la contraseña en texto plano coincide con la contraseña hasheada 
from authenticathion.models import  Entity ,AccountUser #Modelo donde tenemos la cuenta de usuario
from django.contrib.auth.hashers import make_password




class AutenthicathionDishospital(BaseBackend): #Esta nueva clase va a sobreescribir los metodos clave authenticate y get_user() 
      
    

      def authenticate(self,request,tipo_documento = None,numero_documento = None , password = None ):




          try:
             principalUser = Entity.objects.get(identity_document_id = tipo_documento , document_number = numero_documento)
             
             
          except Entity.DoesNotExist:
              
              return None
         
          userPassword = AccountUser.objects.get(entity_id = principalUser.id)
          bd_hash = make_password(userPassword.password_hash)


          print("La contraseña del usuario en la base de datos sin hashear es ",userPassword.password_hash)
          userPassword.password_hash = bd_hash
          
          print("La contraseña del usuario en la base de datos ",userPassword.password_hash)
           



          if check_password(password, userPassword.password_hash):
                print("Las contraseñas son iguales")
                return userPassword

          return None 
      
      def get_user(self,user_id):
            try:
                 return Entity.objects.get(pk=user_id) 
            
            except Entity.DoesNotExist:
                 
                 return None
                   