from django.urls import path
from . import views


app_name = "tickets"

urlpatterns =[
    path('formularios/<str:form>/',views.manejoDeFormatos,name='formatosFormularios'),
    path('formularios/<str:form>/<int:ticket_id>', views.manejoDeFormatos , name='formatosFormulariosLlenar')
]