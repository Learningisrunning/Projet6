from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
   first_name = models.CharField(max_length=40)
   last_name = models.CharField(max_length=50)

   def __str__(self) -> str:
      return self.username + ' ' + str(self.id)

class Project(models.Model):

   class type_possible(models.TextChoices):
      BE = 'Back-end'
      FE = 'front-end'
      IOS = 'IOS'
      Android = 'Android'

   title = models.CharField(max_length=128)
   description = models.CharField(max_length=300)
   type = models.CharField(max_length=40, choices=type_possible.choices)
   author_user = models.ForeignKey(User, on_delete=models.CASCADE)

   def __str__(self) -> str:
      return self.title

class Contributor(models.Model):

   class permission_possible(models.TextChoices):
      Contributeur = 'CONTRIBUTOR'
      Auteur = 'AUTOR'

   user_id = models.IntegerField()
   project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="contributors")
   role = models.CharField(max_length=50)
   permission = models.CharField(max_length=50, choices=permission_possible.choices)

   def __str__(self) -> str:
      return str(self.project_id) +' '+ str(self.user_id)
   

class Issue(models.Model):

   class priority_possible(models.TextChoices):
      F = 'FAIBLE'
      M = 'MOYENNE'
      E = 'ÉLEVÉE'
   
   class balise_possible(models.TextChoices):
      B = 'BUG'
      A = 'AMÉLIORATION'
      T = 'TÂCHE'

   class status_possible(models.TextChoices):
      AF = 'À FAIRE'
      EC = 'EN COURS'
      T = 'TERMINÉ'
    
   title = models.CharField(max_length=40)
   desc = models.CharField(max_length=50)
   tag = models.CharField(max_length=50, choices=balise_possible.choices)
   priority = models.CharField(max_length=60, choices=priority_possible.choices)
   status = models.CharField(max_length=50, choices=status_possible.choices)
   author_user = models.ForeignKey(User, on_delete=models.CASCADE)
   assignee_user = models.ForeignKey(Contributor, on_delete= models.CASCADE)
   project_related = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues', null=True)
   created_time = models.DateTimeField()

   def __str__(self) -> str:
      return self.title


class Comment(models.Model):
   description = models.CharField(max_length=40)
   author_user = models.ForeignKey(User, on_delete= models.CASCADE)
   issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments", null=True)
   created_time = models.DateTimeField(null=True)

   def __str__(self) -> str:
      return self.description

