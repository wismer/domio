from django.db import models
# Create your models here.


class Zipcode(models.Model):
    zipcode = models.CharField(max_length=5, unique=True)
    query_count = models.PositiveIntegerField()
    objects = models.Manager()

    def __str__(self):
        return self.zipcode
