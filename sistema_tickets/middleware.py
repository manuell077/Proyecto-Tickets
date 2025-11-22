from django.db import connection


#Un middleware es un filtro por el que pasa cada vez que se ejecuta un request 

class SetAuditUserMiddleware:  #Esta es la clase de middleware 
      
      def __init__(self, get_response):
          self.get_response = get_response

      def __call__(self, request):

          entity_id = request.session.get("entity_id") #Guardar en el login
          
          
          if entity_id:
              
            try:
                  with connection.cursor() as cursor:
                      cursor.execute("SELECT set_config('app.current_user_id',%s,false)",
                                     [str(entity_id)])

            except Exception as e:
                
                print("Error en auditoria",e)            

          return self.get_response(request)         
                  


