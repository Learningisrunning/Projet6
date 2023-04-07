from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from API.permissions import IsInTheProject
from rest_framework.response import Response
from rest_framework.decorators import api_view
from requests import request


from API.models import Project, Contributor, Issue, Comment
from API.serializers import ProjetsDetailSerializer, ProjetsListSerializer, ContributorDetailSerializer, ContributorListSerializer
from API.serializers import IssueDetailSerializer, IssueListSerializer, CommentDetailSerializer, CommentListSerializer, RegisterSerializer
# Create your views here.

class ProjetsViewset(ModelViewSet):

    """"Mise en place de la vue des projets avec gestion des 
        vue en list et en détail + filtre pour n'afficher 
        que les projets liés à l'utilisateur"""

    serializer_class = ProjetsListSerializer
    detail_serializer_class = ProjetsDetailSerializer
    permission_classes = [IsAuthenticated, IsInTheProject]
    

    def get_queryset(self):
        userID = self.request.user.id
        projet_contrib_liste = []
        contributors = Contributor.objects.all()

        for contributor in contributors:
            if contributor.user_id == userID:
                projet_contrib_liste.append(contributor.project_id.title)
                
        return Project.objects.filter(author_user = userID) | Project.objects.filter(title__in = projet_contrib_liste)
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return self.detail_serializer_class
        return super().get_serializer_class()

class ContributorViewSet(ModelViewSet):

    """Création de la vue des contributeur en liste 
       et en détail. Mise en place de la possibilité 
       d'ajouter un nouveau contributeur"""

    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer
    permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
            
        if self.action != 'retrieve' and self.action != 'destroy':
            list_contrib_of_the_project = []
            project_number = self.kwargs['projets_pk']
            contributors = Contributor.objects.all()

            for contributor in contributors:
                if contributor.project_id.id == int(project_number):
                    list_contrib_of_the_project.append(contributor)
            
            return list_contrib_of_the_project
        else :
            return Contributor.objects.all()
        
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        if self.action == 'create':
            new_contrib = self.serializer_class.create(self, self.request.data)

            return new_contrib
        return super().perform_create(serializer)

class IssuesrViewSet(ModelViewSet):
    
    """Création de la vue des issues en liste 
       et en détail. Mise en place de la possibilité 
       d'ajouter une nouvelle issue"""

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, IsInTheProject]

    def get_queryset(self):
        if self.action != 'retrieve' and self.action != 'destroy' and self.action != 'update':
            list_issues_of_the_project = []
            project_number = self.kwargs['projets_pk']
            issues = Issue.objects.all()

            for issue in issues:
                print(issue.project_related.id)
                if issue.project_related.id == int(project_number):
                    list_issues_of_the_project.append(issue)
            
            return list_issues_of_the_project
        else :
            return Issue.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        if self.action == 'create':
            new_issue = self.serializer_class.create(self, self.request.data, self.request)

            return new_issue
        return super().perform_create(serializer)
    

class CommentViewset(ModelViewSet):

    """Création de la vue des commentaires en liste 
       et en détail. Mise en place de la possibilité 
       d'ajouter un nouveau commentaire"""
    
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated, IsInTheProject]

    def get_queryset(self):

        if self.action != 'retrieve' and self.action != 'destroy' and self.action != 'update':
            list_comment_of_the_project = []
            issue_number = self.kwargs['issues_pk']
            comments = Comment.objects.all()

            for comment in comments:
                print(comment.issue.id)
                if comment.issue.id == int(issue_number):
                    list_comment_of_the_project.append(comment)
            
            return list_comment_of_the_project
        else :
            return Comment.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        if self.action == 'create':
            new_comment = self.serializer_class.create(self, self.request.data, self.request)

            return new_comment
        return super().perform_create(serializer)

@api_view(['POST',])   
def RegisterViewset(request):

    """Création de la vue de la création de compte."""

    if request.method == 'POST':

        serializer = RegisterSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            new_user = serializer.save()
            data['response'] = "Compte créé"
        else:
            serializer.errors
        return Response(data)

