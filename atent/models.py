from django.db import models
import uuid

class Token(models.Model):
    id = models.UUIDField(default = uuid.uuid4 , primary_key = True)
    user_id = models.IntegerField()
    type = models.IntegerField()
    
