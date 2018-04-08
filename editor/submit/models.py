import os

from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings as django_settings

from submit import constants

class Problem(models.Model):
    order = models.IntegerField(default=1, unique=True)
    title = models.CharField(max_length=128)

    content = RichTextUploadingField()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

class Row(models.Model):
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    order = models.IntegerField(default=1)
    lang = models.IntegerField(choices=constants.Language.LANG_CHOICES)
    content = models.CharField(max_length=1000, default='', blank=True)

    def __unicode__(self):
        return '(Row-%s-%s-%s-%s)' % (user, problem, order, lang)

    class Meta:
        unique_together = ('user', 'problem', 'order')

class SpareRow(models.Model):
    user = models.ForeignKey(User)
    lang = models.IntegerField(choices=constants.Language.LANG_CHOICES)

    def __unicode__(self):
        return '(SpareRow-%s-%s-%s)' % (id, user, lang)

class Task(models.Model):
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    active = models.BooleanField()
    solved = models.BooleanField(default=False)
    custom_input = models.TextField(blank=True, default='')

    def __unicode__(self):
        return '(Task-%s-%s-%s)' % (id, user, problem, active)

    class Meta:
        unique_together = ('user', 'problem')

class SubmitOutput(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    status = models.CharField(max_length=128, blank=True,
                              choices=constants.ReviewResponse.all_items_as_choices())
    score = models.IntegerField()
    custom = models.BooleanField(default=False)

    def dir_path(self):
        return os.path.join(django_settings.SUBMIT_PATH, 'submits',
                str(self.user.id), str(self.id))
    
    def verbose_response(self):
        return constants.ReviewResponse.verbose(self.status)

    def file_path(self):
        return os.path.join(self.dir_path(), str(self.id) + constants.SUBMITTED_FILE_EXTENSION)

    def lang_path(self):
        return os.path.join(self.dir_path(), str(self.id) + constants.SUBMITTED_LANG_FILE_EXTENSION)

    def custom_input_path(self):
        return os.path.join(self.dir_path(), str(self.id) + constants.SUBMITTED_CUSTOM_INPUT_FILE_EXTENSION)

    def raw_path(self):
        return os.path.join(self.dir_path(), str(self.id) + constants.TESTING_RAW_EXTENSION)

    def protocol_path(self):
        return os.path.join(self.dir_path(), str(self.id) + constants.TESTING_PROTOCOL_EXTENSION)

    def protocol_exists(self):
        return os.path.exists(self.protocol_path())

    def __unicode__(self):
        return '(Output-%s-%s-%s-%s-%s)' % (timestamp, user, problem, status, custom)


from django.db.models.signals import post_save, pre_save

def pre_save_row(sender, instance, **kwargs):
    lang = int(instance.lang)
    length = constants.Language.LANG_LINE_LENGTH[lang]
    instance.content = instance.content[:length]

def save_problem(sender, instance, created, **kwargs):
    if created:
        for user in User.objects.all():
            active = len(Task.objects.filter(user=user, active=True))
            Task.objects.create(user=user, problem=instance, active= active < constants.ACTIVE_PROBLEMS)

def save_user(sender, instance, created, **kwargs):
    if created:
        for problem in Problem.objects.all():
            Task.objects.create(user=instance, problem=problem, active=problem.order <= constants.ACTIVE_PROBLEMS)

pre_save.connect(pre_save_row, sender=Row)
post_save.connect(save_problem, sender=Problem)
post_save.connect(save_user, sender=User)
