from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField


class FormData(models.Model):
    name = models.CharField(max_length=100,unique=True,null=False)
    description = models.CharField(max_length=100, help_text="This is the grey text")
    data = JSONField(null=False, blank=False)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name