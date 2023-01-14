from django.db import models  



class CheckMemoryModel(models.Model):
    memory_left=models.PositiveSmallIntegerField()
    date=models.DateTimeField(auto_now_add=True)
