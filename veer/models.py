from django.db import models

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=130)
    phone = models.CharField(max_length=12)
    email = models.EmailField(default="gmail.com")
    message = models.TextField(max_length=500, default="")
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name