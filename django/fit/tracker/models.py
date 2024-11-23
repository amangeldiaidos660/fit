from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    chat_id = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.email
    

class WorkoutType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records')
    workout_data = models.JSONField()
    workout_date = models.DateField()

    def __str__(self):
        return f"{self.user.email} - {self.workout_date}"

