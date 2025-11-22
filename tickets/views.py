from django.shortcuts import render

# Create your views here.



def  panelAdmin (request):

    return render(request,'tickets/dashboardPanel.html')