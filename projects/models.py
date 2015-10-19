from django.db import models

#title, description, owner, team, status, tags
class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    #owner = models.ForeignKey(User)
    #team = models.ManyToManyField(User)
    #status = models.ForeignKey(User)
    #tags = models.ManyToManyField(charField, max_length=128)
    #timestamp = models.DateTimeField()
    
