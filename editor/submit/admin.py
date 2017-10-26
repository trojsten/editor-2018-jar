from django.contrib import admin
from submit.models import Problem, Row, ActiveProblem, SubmitOutput

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'order')

class RowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'problem', 'lang', 'order')

class ActiveProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'problem')

class SubmitOutputAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'user', 'problem', 'status')

admin.site.register(Problem, ProblemAdmin)
admin.site.register(Row, RowAdmin)
admin.site.register(ActiveProblem, ActiveProblemAdmin)
admin.site.register(SubmitOutput, SubmitOutputAdmin)

# Register your models here.
