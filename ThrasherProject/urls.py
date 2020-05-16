"""MyProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from ThrasherApp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns 

app_name = 'music'




urlpatterns = [
    # path('', views.index, name='home'),
    path('admin/', admin.site.urls),
    path('music/', views.IndexView.as_view(), name='index'),
    # path('', views.index2, name='index2'),
    path('music/<int:pk>/', views.ConditionView.as_view(), name='param'),
    path('', views.MainpageView.as_view(), name='index2'),

    path('music/album/add/', views.AlbumCreate.as_view(), name='album-add'),
    path('music/album/<int:pk>/', views.AlbumUpdate.as_view(), name='album-update'),
    path('music/album/<int:pk>/delete/', views.AlbumDelete.as_view(), name='album-delete'),

    path('music/<int:pk>/song/add/', views.SongCreate.as_view(), name='song-add'),
    path('music/song/<int:pk>/', views.SongUpdate.as_view(), name='song-update'),
    path('music/song/<int:pk>/delete/', views.SongDelete.as_view(), name='song-delete'),

    path('music/<int:pk>/post/add/', views.PostCreate.as_view(), name='post-add'),
    path('music/post/<int:pk>/', views.PostUpdate.as_view(), name='post-update'),
    path('music/post/<int:pk>/delete/', views.PostDelete.as_view(), name='post-delete'),
    
    path('reviews/', views.ReviewIndexView.as_view(), name='revindex'),
    path('reviews/<int:pk>/', views.ReviewConditionView.as_view(), name='revparam'),
    
    path('reviews/review/add/', views.ReviewCreate.as_view(), name='review-add'),
    path('reviews/review/<int:pk>/', views.ReviewUpdate.as_view(), name='review-update'),
    path('reviews/review/<int:pk>/delete/', views.ReviewDelete.as_view(), name='review-delete'),

    path('reviews/<int:pk>/post/add/', views.ReviewPostCreate.as_view(), name='reviewpost-add'),
    path('reviews/post/<int:pk>/', views.ReviewPostUpdate.as_view(), name='reviewpost-update'),
    path('reviews/post/<int:pk>/delete/', views.ReviewPostDelete.as_view(), name='reviewpost-delete'),

    
    path('music/register/', views.UserFormView.as_view(), name='register'),
    path('loudwire/', views.scrape, name='loud'),
    path('login/', auth_views.LoginView.as_view(template_name='music/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='music/mainpage.html'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='music/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='music/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='music/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='music/password_reset_complete.html'), name='password_reset_complete'),
    path('i18n/', include('django.conf.urls.i18n')),

    # path('music/login_user/', views.UserFormView.as_view(), name='login_user'),

    

]

urlpatterns += i18n_patterns(*urlpatterns, prefix_default_language=False)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


