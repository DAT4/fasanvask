from django.contrib import admin
from .models import Resident, WashTime

@admin.register(Resident)
class RegisterAdmin(admin.ModelAdmin):
    pass
@admin.register(WashTime)
class WashTimeAdmin(admin.ModelAdmin):
    pass
