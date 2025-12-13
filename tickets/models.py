from django.db import models

class concept_low(models.Model):
    id = models.BigAutoField(primary_key=True)
    concept_of_low = models.CharField(255)
    

    class Meta:
        managed = False
        db_table = 'tickets"."concept_low' 

    def __str__(self):
          return f"{self.concept_of_low}"       