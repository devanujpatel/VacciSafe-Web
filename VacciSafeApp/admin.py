from django.contrib import admin
from .models import VaccineRecords, Vaccines, Recipients#
# Register your models here.
admin.site.register(Recipients)
admin.site.register(VaccineRecords)
admin.site.register(Vaccines)