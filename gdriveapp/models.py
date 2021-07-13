from django.db import models

class Content(models.Model):
    fileName=models.CharField(max_length=100,default=None)
    link=models.TextField(default=None)
    content = models.TextField()
def __str__(self):
    return '%s' % (self.name)
