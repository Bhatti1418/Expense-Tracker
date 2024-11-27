from django.contrib import admin
from .models import Items,Balance
# Register your models here.
admin.site.register([Items,Balance])