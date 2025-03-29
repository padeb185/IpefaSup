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

class Employee(Person):
    employee_email = models.EmailField(unique=True)
    matricule = models.CharField(max_length=255)

class Teacher(Employee):
    pass

class Educator(Employee):
    pass




class Section(models.Model):
    wording = models.CharField(max_length=255)

    def __str__(self):
        return self.wording


#Une Section a un wording (nom ou description).

#Une UE (Unité d'Enseignement) a plusieurs attributs (idUE, wording, numberPeriods).

#Une Section peut être associée à plusieurs UEs (relation 0,N).

#Une UE peut avoir plusieurs prérequis (relation récursive 0,N).



class UE(models.Model):
    idUE = models.CharField(max_length=50, unique=True)
    wording = models.CharField(max_length=255)
    numberPeriods = models.IntegerField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='ues')  # Relation 0,N avec Section
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='dependents')  # Relation récursive 0,N

    def __str__(self):
        return f"{self.idUE} - {self.wording}"

#Avec cette approche, tu peux récupérer :

 #   Toutes les UEs d'une section : section_instance.ues.all()

 #   Les prérequis d'une UE : ue_instance.prerequisites.all()

 #   Les UEs qui dépendent d'une UE donnée : ue_instance.dependents.all()



class AcademicUE(UE):  # Hérite de UE
    academicYear = models.CharField(max_length=9)  # Ex: "2024-2025"
    yearCycle = models.IntegerField()

    def type(self):
        return "Academic UE"

    def __str__(self):
        return f"{self.idUE} - {self.wording} ({self.academicYear}, Cycle {self.yearCycle})"


