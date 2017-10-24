from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Problem(models.Model):
    order = models.IntegerField(default=0, unique=True)
    title = models.CharField(max_length=128)

    content = RichTextUploadingField()

    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.title
