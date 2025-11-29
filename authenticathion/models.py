from django.db import models


#Creacion del modelo de la tabla IndentityDocument donde solo necitaremos el code que es "Nit,C.C," y el nombre de este documento
class IndentityDocument(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=80)
    document_name = models.CharField(max_length=80)
    
    
    #la clase meta es como un panel de administracion de los modelos que permite decirle al modelo que no actulice la tabla en la bsae de datos
    class Meta:
        managed = False #Para que no actualice en la base de datos
        db_table = 'core"."identity_document' #haciendo referencia a la tabla en la base de datos 

    def __str__(self):#funcion para cuando se haga referncia a estos objetos en forma de texto se muestren de diferente forma
        return f"{self.code} - {self.document_name}"

#Creacion del modelo de entity donde solo necesitartemos el id , el numero del documento y le nombre completo
class Entity(models.Model):
     id = models.BigAutoField(primary_key=True)
     document_number = models.CharField(max_length=80)
     full_name = models.CharField(max_length=150)
     identity_document_id = models.ForeignKey(IndentityDocument,on_delete=models.DO_NOTHING,db_column="identity_document_id")
     
     class Meta:
          managed = False 
          db_table = 'core"."entity'
    
     def __str__(self):#funcion para cuando se haga referncia a estos objetos en forma de texto se muestren de diferente forma
        return f"{self.document_number} - {self.full_name}"
     

#Creacion del modelo de account user donde solo utilizaremos la contraseña y la ultima vez que se realizo el login

class AccountUser(models.Model):
    entity_id  = models.BigAutoField(primary_key=True)
    password_hash = models.TextField()
    last_login = models.DateTimeField()
    is_active = models.BooleanField(default=True)


    class Meta:
        managed = False 
        db_table = 'auth"."account_user'
    
    @property
    def is_authenticated(self):
        return True

    def __str__(self):#funcion para cuando se haga referncia a estos objetos en forma de texto se muestren de diferente forma
        return f"{self.entity_id}"
    
class Modulo(models.Model):
      id = models.BigAutoField(primary_key=True)
      module_name = models.TextField()

      class Meta:
            managed = False
            db_table = 'auth"."module'

      def __str__(self):
            return f"{self.module_name}"      

class Entity_Permission_Submodule(models.Model):
      entity_id = models.IntegerField()
      submodule_id = models.IntegerField()
      permission_id = models.IntegerField()
      
      class Meta: 
            managed = False
            db_table = 'auth"."user_submodule_permission'

      def __str__(self):
            return f"{"Usuario", self.entity_id}"      

class Submodule(models.Model):
      submodule_name = models.TextField()
      module_id = models.BigIntegerField()

      class Meta:
            managed = False
            db_table = 'auth"."submodule'

      def __str__(self):
            return f"{self.submodule_name}"      