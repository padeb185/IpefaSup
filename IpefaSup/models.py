from django.db import models

class Person(models.Model):
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('O', 'Autre'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    street = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    private_email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
