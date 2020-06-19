from django.conf.urls import url

from . import views
from .models import Actor

# REST FRAMEWORK IMPORTS
from rest_framework.urlpatterns import format_suffix_patterns


app_name = "videos"

urlpatterns = [
    # /videos/
    # url(r'^$', views.index, name='index'),
    #
    # # /videos/scenes
    # url(r'^scenes/$', views.scenes, name='scenes'),
    #
    # # /videos/actors
    # url(r'^actors/$', views.actors, name='actors'),
    #
    # # /videos/scenes/[id]
    # url(r'^scenes/(?P<pk>[0-9]+)/$', views.SceneDetails.as_view(), name='scene-details'),
    #
    # # /videos/actors/[id]
    # url(r'^actors/(?P<pk>[0-9]+)/$', views.ActorDetails.as_view(), name='actor-details'),
    #
    # # /videos/actors/[id]/tags
    # url(r'^actors/(?P<pk>[0-9]+)/tag/$', views.actor_add_tag, name='actor-add-tag'),
    #
    # # /videos/scenes/add
    # url(r'^scenes/add/$', views.add_scenes, name='scenes-add'),
    #
    # # /videos/scenes/add/form
    # url(r'^scenes/add/form$', views.scenes_add_walker, name='scenes-add-walker'),
    #
    # # /videos/actors/add/form
    # url(r'^actors/add-actor/form$', views.ActorAdd.as_view(model=Actor, success_url="/videos/actors"),
    #     name='actors-add-form'),
    #
    # # /videos/actors/add/
    # url(r'^actors/add$', views.actors_add, name='actors-add'),
    # # /videos/actors/add/logic
    # url(r'^a/actors/add/logic$', views.actors_add_logic, name='actors-add-logic'),
    #
    # # /videos/actors/tags/
    # url(r'^actors/tags$', views.actors_tags, name='actors-tags'),
    #
    # # /videos/actors/tags/
    # url(r'^scene/tags$', views.scene_tags, name='scenes-tags'),
    #
    # # /videos/websites/
    # url(r'^websites/$', views.websites, name='websites'),
    #
    # # /videos/websites/details/id
    # url(r'^websites/details/(?P<pk>[0-9]+)/$', views.website_details, name='websites-details'),
    #
    # # /videos/actors/tags/<tag_id>/details
    # url(r'^actors/tags/(?P<pk>[0-9]+)/details/$', views.actors_tag_details, name='actor-tag-details'),
    #
    # # /videos/actors/tags/<tag_id>/details
    # url(r'^scenes/tags/(?P<pk>[0-9]+)/details/$', views.scenes_tag_details, name='scene-tag-details'),
    #
    # # /vidoes/scenes/[id]/add-actor-to-scene
    # url(r'^scenes/(?P<scene_id>[0-9]+)/add_actor$', views.scene_details, name='scene-add-actor'),
    #
    # # /vidoes/ (actor autocomplete)
    # url(r'^actor-autocomplete/$', views.ActorAutocomplete.as_view(create_field='name'), name='actor-autocomplete'),
    #
    # url(r'^actor-alias-autocomplete/$', views.ActorAliasAutocomplete.as_view(create_field='name'),
    #     name='actor-alias-autocomplete'),
    #
    # # /vidoes/ (actor tag autocomplete)
    # url(r'^actor-tag-autocomplete/$', views.ActorTagsAutocomplete.as_view(create_field='name'),
    #     name='actor-tag-autocomplete'),
    #
    # # /vidoes/ (scene tag autocomplete)
    # url(r'^scene-tag-autocomplete/$', views.SceneTagsAutocomplete.as_view(create_field='name'),
    #     name='scene-tag-autocomplete'),
    #
    # # /vidoes/ (website autocomplete)
    # url(r'^website-autocomplete/$', views.WebsiteAutocomplete.as_view(create_field='name'),
    #     name='website-autocomplete'),
    #
    # # /scrape/tmdb/<actor id> scrape actor with tmdb
    # url(r'^scrape/tmdb/(?P<pk>[0-9]+)/$', views.scrape_actor_tmdb,
    #     name='scrape-actor-tmdb'),
    #
    # # /scrape/imdb/<actor id> scrape actor with tmdb
    # url(r'^scrape/imdb/(?P<pk>[0-9]+)/$', views.scrape_actor_imdb,
    #     name='scrape-actor-imdb'),
    #
    # # /scrape/freeones/<actor id> scrape actor with freeones
    # url(r'^scrape/freeones/(?P<pk>[0-9]+)/$', views.scrape_actor_freeones,
    #     name='scrape-actor-freeones'),
    #
    # url(r'^play/scene/(?P<pk>[0-9]+)/$', views.play_scene,
    #     name='play-scene'),
    #
    # url(r'^clean-library/$', views.clean_library,
    #     name='clean-library'),
    #
    # url(r'^settings/$', views.settings, name='settings'),
    #
    # url(r'^scan-all-scenes/$', views.scan_all_scenes, name='scan_all_scenes'),
    #
    # url(r'^folders/$', views.folder_view_tree, name='folder-view-tree'),
    #
    # url(r'^folder/(?P<pk>-{0,1}[0-9]+)/$', views.folder_view, name='folder-view'),
    #   REST-FRAMEWORK-VIEWS
    #
    #     url(r'^rest/$', views.api_root),
    #
    #     url(r'^rest/actor-alias/',
    #         views.ActorAliasListRest.as_view(),
    #         name='actor-alias-list-rest'),
    #
    #     url(r'^rest/actors/',
    #         views.ActorListRest.as_view(),
    #         name='actors-list-rest'),
    #
    #     url(r'^rest/actor-alias/details/(?P<pk>[0-9]+)/', views.ActorAliasDetailsRest.as_view(),
    #         name='actor-alias-details-rest'),
    #
    #     url(r'^rest/actor/details/(?P<pk>[0-9]+)/$',
    #         views.ActorDetailsRest.as_view(),
    #         name='actor-details-rest'),
    #     url(r'^rest/actor-alias/details/(?P<pk>[0-9]+)/html',
    #         views.ActorAliasHTMLRest.as_view(),
    #         name='actor-alias-details-rest'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# startup()
