from rest_framework.permissions import SAFE_METHODS, BasePermission
from API.models import Contributor
       
class IsInTheProject(BasePermission):

    """Mise en place de la permission qui permet de savoir
        si un utilisateur est contributeur ou auteur
        et donc de lui accorder des droits en fonction"""

    message = "Seul l'auteur de ce projet peut modifier/supprimer et seul les contributeurs du projet peuvent voir"

    def has_object_permission(self, request, view, obj):

        author_id = obj.author_user.id
        user_connected = request.user.id
        project_actif_id = request.get_full_path()
        url_infos = project_actif_id.split("/")
        project_actif_id = url_infos[3]
        
        contributors = Contributor.objects.all()

        #On vérifie si le USER fait partie des contributeurs du projet
        for contributor in contributors:
            if contributor.project_id.id == int(project_actif_id) and contributor.user_id == user_connected or author_id == user_connected:
                validation = True
                break
            else:
                validation = False


        list_methods_allow_all = ['GET', 'POST']

        if request.method in list_methods_allow_all:
            return validation
        else :
            return author_id == user_connected
       
