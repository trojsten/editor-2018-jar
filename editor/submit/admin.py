from django.contrib import admin
from submit.models import Problem, Row, SpareRow, SubmitOutput, Task

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'order')

class RowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'problem', 'lang', 'order')

class SpareRowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'lang')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'problem', 'active', 'solved')

class SubmitOutputAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'user', 'problem', 'custom', 'status')

admin.site.register(Problem, ProblemAdmin)
admin.site.register(Row, RowAdmin)
admin.site.register(SpareRow, SpareRowAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(SubmitOutput, SubmitOutputAdmin)

# Register your models here.
