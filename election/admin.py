from django.contrib import admin
from .models import AnnouncedPUResults, PollingUnits, LGAS,Party


# Register your models here.
admin.site.register(AnnouncedPUResults)
admin.site.register(PollingUnits),
admin.site.register(LGAS),
admin.site.register(Party)