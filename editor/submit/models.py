from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User

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
        return "Row-%s-%s-%s-%s" % (user, problem, order, lang)

    class Meta:
        unique_together = ("user", "problem", "order")
