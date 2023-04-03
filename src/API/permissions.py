from rest_framework.permissions import SAFE_METHODS, BasePermission
from API.models import Project, Contributor

class IsAContributors(BasePermission):
    message = 'Seuls les contributeurs peuvent voir le projet'
    
    contributors = Contributor.objects.all()

    def has_object_permission(self, request, view, obj):
       
       print(obj)
       if request.method in SAFE_METHODS:
           return True
       else :
          return obj.user_id == request.user.id
       
class IsInTheProject(BasePermission):
    message = "Seul l'auteur de ce projet peut modifier/supprimer et seul les contributeurs du projet peuvent voir"

    def has_object_permission(self, request, view, obj):

        author_id = obj.author_user.id
        user_connected = request.user.id
        project_actif_id = request.get_full_path()
        url_infos = project_actif_id.split("/")
        project_actif_id = url_infos[3]
        
        contributors = Contributor.objects.all()

        for contributor in contributors:
            if contributor.project_id.id == int(project_actif_id):
                validation = True
            else:
                validation = False


        list_methods_allow_all = ['GET', 'POST']

        if request.method in list_methods_allow_all:
            return validation
        else :
            return author_id == user_connected
       
