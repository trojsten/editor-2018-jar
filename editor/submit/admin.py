from django.contrib import admin
from submit.models import Problem, Row

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'order')

class RowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'problem', 'lang', 'order')

admin.site.register(Problem, ProblemAdmin)
admin.site.register(Row, RowAdmin)

# Register your models here.
