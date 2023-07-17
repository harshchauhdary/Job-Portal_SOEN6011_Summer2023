from django.contrib import admin
from .models import App_user, Job, Resume

# Register your models here.
admin.site.register(App_user)
admin.site.register(Job)
admin.site.register(Resume)
