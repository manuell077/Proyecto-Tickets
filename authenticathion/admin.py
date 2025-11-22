from django.contrib import admin

from .models import *

admin.site.register(IndentityDocument)
admin.site.register(Entity)
admin.site.register(AccountUser)