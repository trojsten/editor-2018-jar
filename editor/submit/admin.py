from django.contrib import admin
from submit.models import Problem

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'order')

admin.site.register(Problem, ProblemAdmin)

# Register your models here.
