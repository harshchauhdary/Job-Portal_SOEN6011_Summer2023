from django.contrib import admin
from .models import Candidate, Job, Resume

# Register your models here.
admin.site.register(Candidate)
admin.site.register(Job)
admin.site.register(Resume)
