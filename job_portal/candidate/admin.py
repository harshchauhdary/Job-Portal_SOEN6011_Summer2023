from django.contrib import admin
from .models import User, Job, Resume, Candidate, Application, Education, Experience, Skill, Project

# Register your models here.
admin.site.register(User)
admin.site.register(Job)
admin.site.register(Candidate)
admin.site.register(Resume)
admin.site.register(Application)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Skill)
admin.site.register(Project)