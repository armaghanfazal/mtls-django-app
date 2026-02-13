from django.db import models

class DataLog(models.Model):
    level = models.CharField(max_length=20)
    message = models.TextField()


    def __str__(self):
        return f"{self.level}: {self.message}"