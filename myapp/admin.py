from django.contrib import admin
from .models import Room, TenantProfile, Payment, MaintenanceRequest, Announcement

admin.site.register(Room)
admin.site.register(TenantProfile)
admin.site.register(Payment)
admin.site.register(MaintenanceRequest)
admin.site.register(Announcement)
