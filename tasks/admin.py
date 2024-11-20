from django.contrib import admin

# Register your models here.
from tasks.models import Tasks

admin.sites.site.register(Tasks)
