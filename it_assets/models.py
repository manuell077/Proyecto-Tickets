from django.db import models
from authenticathion.models import Entity

class device (models.Model):
    id = models.BigAutoField(primary_key=True)
    serial_number = models.CharField()
    entity_id = models.ForeignKey(Entity,on_delete=models.DO_NOTHING,db_column="entity_id")

    class Meta:
        managed = False
        db_table = 'it_assets"."device'

    def __str__(self):
          return f"{self.serial_number}"     

