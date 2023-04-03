from rest_framework.serializers import ModelSerializer, EmailField, CharField
from rest_framework.validators import UniqueValidator, ValidationError
from django.contrib.auth.password_validation import validate_password
from datetime import datetime
from API.models import Project, Contributor, Comment, Issue, User


class ContributorListSerializer(ModelSerializer):

    """Mise en place du sérializer des contributeurs et création de la fonction create()
        permettant l'ajout d'un contributeur"""

    class Meta:
        model = Contributor
        fields = ['id', 'user_id']
    
    def create(self, validated_data):
        
        project_id = validated_data['project_id_id']
        projects = Project.objects.all()

        new_contrib = Contributor()
        for project in projects:
            if project.id == project_id:
                new_contrib.user_id = validated_data['user_id']
                new_contrib.role = validated_data['role']
                new_contrib.permission = validated_data['permission']
                new_contrib.project_id = project

                new_contrib.save()

                return new_contrib

class ContributorDetailSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'user_id','role', 'permission']

class CommentListSerializer(ModelSerializer):

    """Mise en place du sérializer des comments et création de la fonction create()
        permettant l'ajout d'un comment"""

    class Meta:
        model = Comment
        fields = ['id', 'created_time', 'description']

    def create(self, validated_data, request):
        

        issue_receive = self.kwargs['issues_pk']
        issues = Issue.objects.all()

        new_comment = Comment()
        for issue in issues:
            if int(issue_receive) == issue.id:

                new_comment.description = validated_data['description']
                new_comment.author_user = request.user
                new_comment.issue = issue
                new_comment.created_time = datetime.now()

                new_comment.save()

                return new_comment

class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id','author_user', 'created_time', 'description']

class IssueListSerializer(ModelSerializer):
    """Mise en place du sérializer des issues et création de la fonction create()
        permettant l'ajout d'une issue"""
    class Meta:
        model = Issue
        fields = ['id', 'title', 'tag', 'priority']
    
    def create(self, validated_data, request):
        
        project_id = self.kwargs['projets_pk']
        projects = Project.objects.all()

        assignee_user = validated_data['assignee_user']
        contributors = Contributor.objects.all()

        for contributor in contributors:
            if assignee_user == contributor.user_id:
                assignee_user = contributor
                break

        new_issue = Issue()
        for project in projects:
            if project.id == int(project_id):
                new_issue.title = validated_data['title']
                new_issue.desc = validated_data['desc']
                new_issue.tag = validated_data['tag']
                new_issue.priority = validated_data['priority']
                new_issue.status = validated_data['status']
                new_issue.author_user = request.user
                new_issue.assignee_user = assignee_user
                new_issue.project_related = project
                new_issue.created_time = datetime.now()

                new_issue.save()

                return new_issue

class IssueDetailSerializer(ModelSerializer):

    comments = CommentDetailSerializer(many = True)
    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'status', 'author_user', 'assignee_user', 'created_time', 'comments']

class ProjetsListSerializer(ModelSerializer):


    class Meta:
        model = Project
        fields = ['id', 'title', 'author_user']
    

class ProjetsDetailSerializer(ModelSerializer):

    contributors = ContributorDetailSerializer(many = True)
    class Meta:
        model = Project
        fields = ['id', 'title', 'author_user', 'contributors', 'issues']
    

class RegisterSerializer(ModelSerializer):

    """Création du serializer de création de compte
        Utilisant la base du model USER. Creation de la fonction SAVE()"""

    password2 = CharField(style={'input_type' : 'password'}, write_only = True)

    class Meta: 
        model = User
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name' ]
        extra_kwargs = {
            'password' : {'write_only' : True}
        }
    
    def save(self):
        user = User(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],

        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2 : 
            raise ValidationError({'password' : 'les mdp doivent être identiques' })
        
        user.set_password(password)
        user.save()
        return user 