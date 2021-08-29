from turtle import title
import uuid
from django.db import models

class Director(models.Model):
  id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)

  def __str__(self):
    return f'{self.first_name} {self.last_name}'


class Movie(models.Model):
  id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
  title = models.CharField(max_length=200)
  year = models.IntegerField(default=2000)
  director = models.ForeignKey(Director, on_delete=models.PROTECT, blank=True, null=True)

  def __str__(self):
    return f'{self.title} {self.id}'

