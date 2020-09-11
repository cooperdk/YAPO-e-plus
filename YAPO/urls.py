"""YAPO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from videos import views
from configuration import Config

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'actor-alias', views.ActorAliasViewSet)
router.register(r'actor', views.ActorViewSet)
router.register(r'actor-tag', views.ActorTagViewSet)
router.register(r'scene', views.SceneViewSet)
router.register(r'scene-tag', views.SceneTagViewSet)
router.register(r'website', views.WebsiteViewSet)
router.register(r'folder', views.FolderViewSet)
router.register(r'folder-local', views.LocalSceneFoldersViewSet)
router.register(r'playlist', views.PlaylistViewSet)

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^videos/', include('videos.urls')),
                  url(r'^api/', include(router.urls)),
                  url(r'^$', views.angular_index, name='angular-index'),
                  url(r'^upload/', views.AssetAdd.as_view()),
                  url(r'^scrape-actor/', views.ScrapeActor.as_view()),
                  url(r'^play-scene/', views.play_in_vlc),
                  url(r'^open-folder/', views.OpenFolder.as_view()),
                  url(r'^add-items/', views.AddItems.as_view()),
                  url(r'^settings/', views.settings),
                  url(r'^ffmpeg/', views.ffmpeg),
                  url(r'^tag-multiple-items/', views.tag_multiple_items),
                  url(r'^play/', views.display_video),
                  url(r'^scan-scene/', views.scanScene.as_view()),
              ] + static(Config().site_media_url, document_root=Config().site_media_path)
