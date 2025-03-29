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

    class Meta:
        abstract = True  # Empêche la création d'une table Person


class Employee(Person):
    employee_email = models.EmailField(unique=True)
    matricule = models.CharField(max_length=255)

    class Meta:
        abstract = True  # Empêche la création de la table Employee

class Teacher(Employee):
    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.employee_email}"

class Educator(Employee):
    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.employee_email}"

class Student(Person):  # Hérite de Person
    studentMail = models.EmailField(unique=True)  # Email étudiant
    sessions = models.ManyToManyField('Session', related_name='students',
                                      blank=True)  # Relation ManyToMany avec Session
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.studentMail})"


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
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='academic_ues')  # Relation 0,1 vers Teacher
    def type(self):
        return "Academic UE"

    def __str__(self):
        return f"{self.idUE} - {self.wording} ({self.academicYear}, Cycle {self.yearCycle})"


#Si tu as un lien de composition (♦ noire) entre AcademicUE et Session, cela signifie que :

 #   Une AcademicUE contient des Sessions.

 #   Une Session ne peut pas exister sans une AcademicUE.

 #   Si une AcademicUE est supprimée, toutes ses Sessions sont supprimées aussi.



class Session(models.Model):
    jour = models.IntegerField()  # 1 à 31
    mois = models.IntegerField()  # 1 à 12
    academicUE = models.ForeignKey(AcademicUE, on_delete=models.CASCADE, related_name='sessions')  # Composition

    def __str__(self):
        return f"Session le {self.jour}/{self.mois} pour {self.academicUE.wording}"



# Création d'une section
# section = Section.objects.create(wording="Sciences")

# Création d'une AcademicUE
# academic_ue = AcademicUE.objects.create(idUE="MATH101", wording="Mathématiques", numberPeriods=30,
                                       # section=section, academicYear="2024-2025", yearCycle=1)

# Ajout de sessions
#session1 = Session.objects.create(jour=15, mois=6, academicUE=academic_ue)
#session2 = Session.objects.create(jour=20, mois=12, academicUE=academic_ue)

# Afficher les sessions d'une UE
#for session in academic_ue.sessions.all():
#    print(session)
