from django.contrib import admin
from submit.models import Problem, Row, SpareRow, ActiveProblem, SubmitOutput

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'order')

class RowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'problem', 'lang', 'order')

class SpareRowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'lang')

class ActiveProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'problem')

class SubmitOutputAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'user', 'problem', 'status')

admin.site.register(Problem, ProblemAdmin)
admin.site.register(Row, RowAdmin)
admin.site.register(SpareRow, SpareRowAdmin)
admin.site.register(ActiveProblem, ActiveProblemAdmin)
admin.site.register(SubmitOutput, SubmitOutputAdmin)

# Register your models here.
