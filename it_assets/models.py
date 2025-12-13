from django.db import models

class device (models.Model):
    id = models.BigAutoField(primary_key=True)
    serial_number = models.CharField()
    division_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'it_assets"."device'

    def __str__(self):
          return f"{self.serial_number}"     

