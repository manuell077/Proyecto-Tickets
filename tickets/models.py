from django.db import models
from authenticathion.models import  Entity ,AccountUser
from it_assets.models import device
from core.models import  area
from authenticathion.models import Division
ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En proceso', 'En proceso'),
        ('Revisado', 'Revisado'),
        ('Terminado', 'Terminado'),
]


class concept_low(models.Model):
    id = models.BigAutoField(primary_key=True)
    concept_of_low = models.CharField(255)
    

    class Meta:
        managed = False
        db_table = 'tickets"."concept_low' 

    def __str__(self):
          return f"{self.concept_of_low}"       
    
class header(models.Model):
      code = models.CharField()
      version = models.DecimalField(max_digits=10,decimal_places= 1)
      date_update = models.DateField()
      subprocces = models.CharField()
      procces = models.CharField()
      format = models.CharField()

      class Meta:
        managed = False
        db_table = 'tickets"."header'


      
class tickets(models.Model):
     id = models.BigAutoField(primary_key=True)
     title = models.TextField()
     current_state = models.TextField(choices=ESTADOS)
     account_user_entity_id =  models.ForeignKey(AccountUser,on_delete=models.DO_NOTHING,db_column="account_user_entity_id")

     class Meta:
        managed = False
        db_table = 'tickets"."ticket'
    
class low_team_format(models.Model):
      id = models.BigAutoField(primary_key=True)
      name_authorizes = models.CharField()
      description = models.TextField()
      authorized_siganture = models.TextField()
      responsable_name = models.CharField()
      responsable_signature = models.TextField()
      date_format = models.DateField() 
      concept_low_id = models.ForeignKey(concept_low,on_delete=models.DO_NOTHING,db_column="concept_low_id")
      header_id = models.ForeignKey(header,on_delete=models.DO_NOTHING,db_column="header_id")
      device_id = models.ForeignKey(device,on_delete=models.DO_NOTHING,db_column="device_id")
      ticket_id = models.OneToOneField(tickets,on_delete=models.DO_NOTHING,db_column="ticket_id",related_name="low_team")
      created_at = models.DateTimeField()      

      class Meta:
        managed = False
        db_table = 'tickets"."low_team_format'

class equipment_delivery_format(models.Model):
     id = models.BigAutoField(primary_key=True) 
     observations = models.TextField()
     loan_date = models.DateField()
     return_date = models.DateField()
     received_siganture = models.TextField()
     returned_signature = models.TextField()
     entity_id = models.ForeignKey(Entity,on_delete=models.DO_NOTHING,db_column="entity_id")
     header_id = models.ForeignKey(header,on_delete=models.DO_NOTHING,db_column="header_id")
     ticket_id = models.OneToOneField(tickets,on_delete=models.DO_NOTHING,db_column="ticket_id",related_name="equipment_delivery")
     created_at = models.DateTimeField()   

     class Meta:
        managed = False
        db_table = 'tickets"."equipment_delivery_format'

class request_tics(models.Model):
      id = models.BigAutoField(primary_key=True)
      impact = models.TextField()
      class_new = models.BooleanField()
      priority = models.TextField()
      justification = models.TextField()
      description  = models.TextField()
      exchange_rate = models.TextField() 
      date_request = models.DateField()
      header_id = models.ForeignKey(header,on_delete=models.DO_NOTHING,db_column="header_id")
      ticket_id = models.OneToOneField(tickets,on_delete=models.DO_NOTHING,db_column="ticket_id",related_name="request_tics")
      created_at = models.DateTimeField()   

      class Meta:
          managed = False
          db_table = 'tickets"."request_tics'

class work_plan(models.Model):
    id = models.BigAutoField(primary_key=True)
    number_work_plan  = models.IntegerField()
    activity = models.CharField()
    resource_description = models.CharField()
    start_work_plan = models.DateField()
    end_work_plan = models.DateField()      
    entity_id = models.ForeignKey(Entity,on_delete=models.DO_NOTHING,db_column="entity_id")
    request_tics_id = models.ForeignKey(request_tics,on_delete=models.DO_NOTHING,db_column="request_tics_id")
    
    class Meta:
          managed = False
          db_table = 'tickets"."work_plan'
  
class response_data(models.Model):
     id = models.BigAutoField(primary_key=True)
     date_data = models.DateField()
     request_tics_id = models.ForeignKey(request_tics,on_delete=models.DO_NOTHING,db_column="request_tics_id")
     user_id = models.ForeignKey(AccountUser,on_delete=models.DO_NOTHING,db_column="user_id")
     status_request = models.BooleanField()

     class Meta:
          managed = False
          db_table = 'tickets"."response_data'

class area_request_tics(models.Model):
      id = models.BigAutoField(primary_key=True)
      area_id = models.ForeignKey(area,on_delete=models.DO_NOTHING,db_column="area_id")
      request_tics_id = models.ForeignKey(request_tics,on_delete=models.DO_NOTHING,db_column="request_tics_id")
      
      class Meta:
          managed = False
          db_table = 'tickets"."area_request_tics'

class hadware_revision_format(models.Model):
     id = models.BigAutoField(primary_key=True)
     date_format = models.DateField()
     description = models.TextField()
     diagnostic = models.TextField()
     solve = models.BooleanField(default=False)
     buy_new = models.BooleanField(default=False)
     buy_spare_part = models.BooleanField(default=False)
     estimated_time = models.DateTimeField()
     reviewed_internal_area = models.BooleanField()
     header_id  = models.ForeignKey(header,on_delete=models.DO_NOTHING,db_column="header_id")
     device_id  = models.ForeignKey(device,on_delete=models.DO_NOTHING,db_column="device_id")
     ticket_id = models.OneToOneField(tickets,on_delete=models.DO_NOTHING,db_column="ticket_id",related_name="hadware_revision")
     created_at = models.DateTimeField() 

     class Meta:
          managed = False
          db_table = 'tickets"."hadware_revision_format'

class authorizathion_hadware(models.Model):
     id = models.BigAutoField(primary_key=True)
     hadware_format_id = models.ForeignKey(hadware_revision_format,on_delete=models.DO_NOTHING,db_column="hadware_format_id")
     date_authorizathion = models.DateField()
     authorizathion = models.BooleanField()
     signature = models.TextField()
     observation = models.TextField()
     area_id = models.ForeignKey(area,on_delete=models.DO_NOTHING,db_column="area_id")

     class Meta:
          managed = False
          db_table = 'tickets"."authorizathion_hadware'

class history_status(models.Model):
      id = models.BigAutoField(primary_key=True)
      ticket_id = models.ForeignKey(tickets,on_delete=models.DO_NOTHING,db_column="ticket_id", related_name="historial")
      state_change = models.TextField()
      date_change = models.DateField()
      observation = models.TextField()

      class Meta:
          managed = False
          db_table = 'tickets"."history_status'

