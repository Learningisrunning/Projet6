from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from API.permissions import IsAContributors, IsInTheProject
from rest_framework.response import Response
from rest_framework.decorators import api_view
from requests import request


from API.models import Project, Contributor, Issue, Comment
from API.serializers import ProjetsDetailSerializer, ProjetsListSerializer, ContributorDetailSerializer, ContributorListSerializer
from API.serializers import IssueDetailSerializer, IssueListSerializer, CommentDetailSerializer, CommentListSerializer, RegisterSerializer
# Create your views here.

class ProjetsViewset(ModelViewSet):

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

    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
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
    
    
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, IsInTheProject]

    def get_queryset(self):
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

    
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated, IsInTheProject]

    def get_queryset(self):
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
    if request.method == 'POST':

        serializer = RegisterSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            new_user = serializer.save()
            data['response'] = "Compte créé"
        else:
            serializer.errors
        return Response(data)

