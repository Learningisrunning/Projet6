"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from requests import request

from API.views import ProjetsViewset, ContributorViewSet, IssuesrViewSet, CommentViewset, RegisterViewset

#router projets
router = routers.SimpleRouter()
router.register('projets', ProjetsViewset , basename = 'projets')

#router contrib
router_contributors = routers.NestedSimpleRouter(router, r'projets', lookup = 'projets')
router_contributors.register(r'contributors', ContributorViewSet, basename='contributors')

#router Issue
router_issue = routers.NestedSimpleRouter(router, r'projets', lookup = 'projets')
router_issue.register(r'issues', IssuesrViewSet , basename='issues')

#router comment 
router_comment = routers.NestedSimpleRouter(router_issue, r'issues', lookup = 'issues')
router_comment.register(r'comments', CommentViewset, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-auth/signup', RegisterViewset),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/', include(router.urls)),
    path('api/', include(router_contributors.urls)),
    path('api/', include(router_issue.urls)),
    path('api/', include(router_comment.urls)),
    

]
