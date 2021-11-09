from django.db import models
import uuid

# Create your models here.
class InputField(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    label = models.CharField(max_length=100)
    form_id = models.UUIDField()

class Form(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    user_id = models.IntegerField()


class Response(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    form_id = models.UUIDField()

class ResponseQuestion(models.Model):
    question_id = models.UUIDField()
    response = models.CharField(max_length=255)
    response_id = models.UUIDField()
