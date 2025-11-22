from django.urls import path
from . import views


app_name = "authenticathion"

urlpatterns =[
    path('',views.loginDishospital,name='login'),
]

