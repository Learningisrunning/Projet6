from django.contrib import admin
from API.models import User, Issue, Comment, Contributor, Project
# Register your models here.
admin.site.register(User)
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(Contributor)
admin.site.register(Project)