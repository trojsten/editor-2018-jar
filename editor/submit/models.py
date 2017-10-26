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
    CPP = 1
    PYTHON = 2
    JAVA = 3
    LANG_CHOICES = (
            (CPP, 'C++'),
            (PYTHON, 'Python'),
            (JAVA, 'Java'),
    )

    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    order = models.IntegerField(default=1)
    lang = models.IntegerField(choices=LANG_CHOICES)
    content = models.CharField(max_length=80, default="")

    def __unicode__(self):
        return "(Row-%s-%s-%s-%s)" % (user, problem, order, lang)

    class Meta:
        unique_together = ("user", "problem", "order")

class ActiveProblem(models.Model):
    user = models.OneToOneField(User)
    problem = models.ForeignKey(Problem)

class SubmitOutput(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    status = models.CharField(max_length=128, blank=True,
                              choices=constants.ReviewResponse.all_items_as_choices())
    score = models.IntegerField()

    def dir_path(self):
        return os.path.join(django_settings.SUBMIT_PATH, 'submits',
                str(self.user.id), str(self.id))


    def file_path(self):
        return os.path.join(self.dir_path(), str(self.id) + constants.SUBMITTED_FILE_EXTENSION)

    def raw_path(self):
        return os.path.join(self.dir_path(), str(self.id) + constants.TESTING_RAW_EXTENSION)

    def protocol_path(self):
        return os.path.join(self.dir_path(), str(self.id) + constants.TESTING_PROTOCOL_EXTENSION)

    def __unicode__(self):
        return "(Output-%s-%s-%s-%s)" % (timestamp, user, problem, status)
