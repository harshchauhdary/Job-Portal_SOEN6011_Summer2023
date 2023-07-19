from django.contrib import admin
from .models import User, Job, Resume, Candidate, Application

# Register your models here.
admin.site.register(User)
admin.site.register(Job)
admin.site.register(Candidate)
admin.site.register(Resume)
admin.site.register(Application)
