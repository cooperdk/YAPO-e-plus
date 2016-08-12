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
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from videos import views
from django.conf import settings
from django.conf.urls.static import static

# actor_alias_list = ActorAliasViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
#
#
# actor_alias_detail = ActorAliasViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
#
# actor_list = ActorViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
#
# actor_detail = ActorViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })



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
# router.register(r'^upload/(?P<filename>[^/]+)', views.FileUploadView.as_view())


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^videos/', include('videos.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^$', views.angualr_index, name='angular-index'),
    url(r'^upload/', views.AssetAdd.as_view()),
    url(r'^scrape-actor/', views.ScrapeActor.as_view()),
    url(r'^play-scene/', views.PlayInVlc.as_view()),
    url(r'^open-folder/', views.OpenFolder.as_view()),
    url(r'^add-items/', views.AddItems.as_view()),
    url(r'^settings/', views.settings),
    url(r'^ffmpeg/', views.ffmpeg),
    url(r'^tag-multiple-items/', views.tag_multiple_items),

    # REST FRAMEWORK

    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # url(r'^rest/api$', views.api_root),

    # url(r'^rest/actor-alias/',
    #     views.ActorAliasListRest.as_view(),
    #     name='actor-alias-list-rest'),
    #
    # url(r'^rest/actors/',
    #     views.ActorListRest.as_view(),
    #     name='actors-list-rest'),
    #
    # url(r'^rest/actor-alias/details/(?P<pk>[0-9]+)/', views.ActorAliasDetailsRest.as_view(),
    #     name='actor-alias-details-rest'),
    #
    # url(r'^rest/actor/details/(?P<pk>[0-9]+)/$',
    #     views.ActorDetailsRest.as_view(),
    #     name='actor-details-rest'),
    # url(r'^rest/actor-alias/details/(?P<pk>[0-9]+)/html',
    #     views.ActorAliasHTMLRest.as_view(),
    #     name='actor-alias-details-rest'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
