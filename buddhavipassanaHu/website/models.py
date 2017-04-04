from django.db import models

# Create your models here.
class WebsiteRegister(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=250)
    message = models.TextField(max_length=10000)

    def __str__(self):
        return self.first_name + self.last_name
