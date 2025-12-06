from django.db import models
   
class Modulo(models.Model):
      id = models.BigAutoField(primary_key=True)
      module_name = models.TextField()

      class Meta:
            managed = False
            db_table = 'auth"."module'

      def __str__(self):
            return f"{self.module_name.upper()}"      

class Entity_Permission_Submodule(models.Model):
      entity_id = models.BigIntegerField()
      submodule_id = models.BigIntegerField()
      permission_id = models.BigIntegerField()
      
      class Meta: 
            managed = False
            db_table = 'auth"."user_submodule_permission'
            unique_together = ('entity_id', 'submodule_id', 'permission_id')
      def __str__(self):
            return f"{"Usuario", self.entity_id}"      

class Submodule(models.Model):
      id = models.BigAutoField(primary_key=True)
      submodule_name = models.TextField()
      module_id = models.BigIntegerField()

      class Meta:
            managed = False
            db_table = 'auth"."submodule'

      def __str__(self):
            return f"{self.submodule_name}"      


