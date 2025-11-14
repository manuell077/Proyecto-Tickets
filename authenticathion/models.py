from django.db import models


#Creacion del modelo de la tabla IndentityDocument
class IndentityDocument(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=80)
    document_name = models.CharField(max_length=80)
    requires_check_digit = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField() 
    updated_by = models.BigIntegerField(null=True,blank=True)
    updated_at = models.DateTimeField(null=True,blank=True)
    
    #la clase meta es como un panel de administracion de los modelos que permite decirle al modelo que no actulice la tabla en la bsae de datos
    class Meta:
        managed = False #Para que no actualice en la base de datos
        db_table = 'core.identity_document' #haciendo referencia a la tabla en la base de datos 

    

