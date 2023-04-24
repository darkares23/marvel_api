from django.db import models

class Character(models.Model):
    marvel_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    thumbnail = models.URLField()

    def __str__(self):
        return self.name