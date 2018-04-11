from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from submit.models import Problem, Row, SpareRow, SubmitOutput, Task, Profile

@admin.register(Problem)
class ProblemAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'id')

@admin.register(Row)
class RowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'problem', 'lang', 'order')

@admin.register(SpareRow)
class SpareRowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'lang')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'problem', 'active', 'solved')

@admin.register(SubmitOutput)
class SubmitOutputAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'user', 'problem', 'custom', 'status')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_player')
    list_editable = ('is_player',)

