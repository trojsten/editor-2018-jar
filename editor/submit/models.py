import os

from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings as django_settings
from django.dispatch import receiver

from submit import constants
from submit.helpers import get_default_custom_input

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_player = models.BooleanField(default=True)

    def __str__(self):
        return '(Profile-%s-%s-%s)' % (self.id, self.user, self.is_player)

class Problem(models.Model):
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    title = models.CharField(max_length=128)

    content = RichTextUploadingField()
    variables = models.TextField(default='{}')

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['order']

class Row(models.Model):
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    order = models.IntegerField(default=1)
    lang = models.IntegerField(choices=constants.Language.LANG_CHOICES)
    content = models.CharField(max_length=1000, default='', blank=True)

    def __str__(self):
        return '(Row-%s-%s-%s-%s)' % (self.user, self.problem, self.order, self.lang)

    class Meta:
        unique_together = ('user', 'problem', 'order')

class SpareRow(models.Model):
    user = models.ForeignKey(User)
    lang = models.IntegerField(choices=constants.Language.LANG_CHOICES)

    def __str__(self):
        return '(SpareRow-%s-%s-%s)' % (self.id, self.user, self.lang)

class Task(models.Model):
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    solved = models.BooleanField(default=False)
    custom_input = models.TextField(blank=True, default='')

    @property
    def active(self):
        if self.solved:
            return False
        order = self.problem.order
        cnt_solved = Task.objects.filter(user=self.user, solved=True, problem__order__lt=order).count()
        if order <= constants.ACTIVE_PROBLEMS + cnt_solved:
            return True
        return False

    def __str__(self):
        return '(Task-%s-%s-%s)' % (self.id, self.user, self.problem, self.active)

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

    def __str__(self):
        return '(Output-%s-%s-%s-%s-%s)' % (self.timestamp, self.user, self.problem, self.status, self.custom)


from django.db.models.signals import post_save, pre_save

@receiver(pre_save, sender=Row)
def pre_save_row(sender, instance, **kwargs):
    lang = int(instance.lang)
    length = constants.Language.LANG_LINE_LENGTH[lang]
    instance.content = instance.content[:length]

@receiver(post_save, sender=Problem)
def save_problem(sender, instance, created, **kwargs):
    if created:
        for user in User.objects.all():
            Task.objects.create(user=user, problem=instance, custom_input=get_default_custom_input(instance))

@receiver(post_save, sender=User)
def save_user(sender, instance, created, **kwargs):
    if created:
        for problem in Problem.objects.all():
            Task.objects.create(user=instance, problem=problem, custom_input=get_default_custom_input(problem))


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
