"""Clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from blog import views
#path('blog/', include('blog.urls')),
urlpatterns = [
    path('admin/', admin.site.urls),
    path('about',views.About.as_view(),name='about'),
    path('',views.PostListView.as_view(),name='main'),
    path('<int:pk>',views.PostDetailView.as_view(), name = 'post_detail'),
    path('new', views.PostCreateView.as_view(),name = 'post_create'),
    path('edit<int:pk>', views.PostUpdateView.as_view(), name = 'post_edit'),
    path('remove<int:pk>', views.PostDeleteView.as_view(), name = 'post_delete'),
    path('drafts', views.DraftListView.as_view(), name = 'post_draft_list'),
    path('post/<int:pk>/comment', views.add_comment_to_post, name = 'add_comment_to_post'),
    path('comment/<int:pk>/approve', views.comment_approve, name = 'comment_aprove'),
    path('comment/<int:pk>/remove', views.comment_remove, name = 'comment_remove'),
    path('post/<int:pk>/publish',views.post_publish, name = 'post_publish'),
    path('accounts/login/', auth_views.LoginView.as_view() , name ='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view() , name = 'logout'),
]
#next_page indicates the page to be redirected to after logging out