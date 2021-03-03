import json

from rest_framework import serializers

from videos.models import *


class SettingsSerializer(serializers.Serializer):
    def to_representation(self, value):
        # class Payload(object):
        #     def __init__(self, j):
        #         self.__dict__ = json.loads(j)

        """
        Args:
            value:
        """
        x = json.loads(value)
        #print ("SERIALIZER: " + str(x))
        return x


class LocalSceneFoldersSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalSceneFolders
        fields = "__all__"


class PathWithIds(serializers.CharField):
    def to_representation(self, value):
        # class Payload(object):
        #     def __init__(self, j):
        #         self.__dict__ = json.loads(j)

        """
        Args:
            value:
        """
        x = json.loads(value)
        # print (x)
        return x


class FolderSerializer(serializers.ModelSerializer):
    path_id = PathWithIds(source="path_with_ids")

    class Meta:
        model = Folder
        fields = [
            "id",
            "level",
            "name",
            "last_folder_name_only",
            "parent",
            "scenes",
            "path_id",
            "date_added",
        ]
        # fields = ['name', 'path_id']


class SceneIdNameSerializer(serializers.ModelSerializer):
    # actorss = ActorListSerializer(source='actors')

    class Meta:
        model = Scene
        depth = 1
        # fields = ['id', 'name', 'path_to_file', 'path_to_dir', 'date_added', 'date_fav', 'date_runner_up', 'play_count',
        #           'is_fav', 'is_runner_up', 'rating', 'description', 'thumbnail', 'scene_tags', 'actors', 'websites' ]
        fields = ["id", "name"]


class SceneTagIdNameSerialzier(serializers.ModelSerializer):
    usage_count = serializers.SerializerMethodField()

    class Meta:
        model = SceneTag
        fields = ["id", "name", "usage_count", "play_count"]

    def get_usage_count(self, obj):
        """
        Args:
            obj:
        """
        return obj.scenes.count()


class WebsiteSerializer(serializers.ModelSerializer):
    # scenes = SceneIdNameSerializer(read_only=True, many=True)
    scene_tags_with_names = SceneTagIdNameSerialzier(
        many=True, read_only=True, source="scene_tags"
    )

    class Meta:
        model = Website
        fields = [
            "id",
            "name",
            "date_added",
            "play_count",
            "date_fav",
            "date_runner_up",
            "is_fav",
            "is_runner_up",
            "rating",
            "thumbnail",
            "url",
            "tpdb_id",
            "scenes",
            "website_alias",
            "exclusions",
            "scene_tags",
            "scene_tags_with_names",
            "filename_format",
        ]


class WebsiteIdNameSerailzier(serializers.ModelSerializer):
    scene_tags_with_names = SceneTagIdNameSerialzier(
        many=True, read_only=True, source="scene_tags"
    )
    usage_count = serializers.SerializerMethodField()

    class Meta:
        model = Website
        fields = ["id", "name", "scene_tags_with_names", "usage_count", "play_count"]

    def get_usage_count(self, obj):
        """
        Args:
            obj:
        """
        return obj.scenes.count()


class SceneTagSerializer(serializers.ModelSerializer):
    # scenes = SceneIdNameSerializer(many=True, read_only=True)

    class Meta:
        model = SceneTag
        fields = [
            "id",
            "name",
            "date_added",
            "play_count",
            "date_fav",
            "date_runner_up",
            "is_fav",
            "is_runner_up",
            "rating",
            "thumbnail",
            "websites",
            "scenes",
            "scene_tag_alias",
            "exclusions",
        ]


class ActorAliasSerializer(serializers.ModelSerializer):
    # actor = serializers.HyperlinkedRelatedField(read_only=`True`, view_name='actor-detail')

    # url = serializers.HyperlinkedIdentityField(view_name='actoralias-detail')

    class Meta:
        model = ActorAlias
        fields = ["id", "name", "is_exempt_from_one_word_search"]


class ActorTagListSerializer(serializers.ModelSerializer):
    # actors = ActorIdNameSerializer(many=True, read_only=True)
    scene_tags = SceneTagIdNameSerialzier(many=True, read_only=True)

    usage_count = serializers.SerializerMethodField()

    class Meta:
        model = ActorTag
        fields = ["id", "name", "scene_tags", "usage_count"]

    def get_usage_count(self, obj):
        """
        Args:
            obj:
        """
        return obj.actors.count()


class ActorIdNameSerializer(serializers.ModelSerializer):
    actor_tags = ActorTagListSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ["id", "name", "thumbnail", "actor_tags"]


class ActorIdNameMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "name"]


class ActorListSerializer(serializers.ModelSerializer):
    actor_tags = ActorTagListSerializer(many=True, read_only=True)
    usage_count = serializers.SerializerMethodField()

    class Meta:
        model = Actor
        fields = [
            "id",
            "name",
            "tpdb_id",
            "thumbnail",
            "rating",
            "height",
            "ethnicity",
            "weight",
            "country_of_origin",
            "is_runner_up",
            "actor_tags",
            "usage_count",
            "play_count",
        ]

    def get_usage_count(self, obj):
        """
        Args:
            obj:
        """
        return obj.scenes.count()


class ActorSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='actor-detail')

    # alias = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='actor-alias-details-rest',
    #                                             lookup_field='actor-alias')

    # actor_aliases = ActorAliasSerializer()

    # actor_aliases = serializers.HyperlinkedRelatedField(allow_null=True, many=True, queryset=ActorAlias.objects.all(),
    #                                                     required=False, view_name='actor-alias-details-rest')

    # scenes = SceneIdNameSerializer(many=True, read_only=True)
    # actor_tags = ActorIdNameSerializer(many=True, read_only=True)

    actor_tags = ActorTagListSerializer(many=True, read_only=True)
    actor_aliases = ActorAliasSerializer(many=True, read_only=True)
    
    class Meta:
        model = Actor
        #depth = 2
        fields = [
            "id",
            "name",
            "date_added",
            "date_fav",
            "date_runner_up",
            "date_of_birth",
            "play_count",
            "is_fav",
            "is_runner_up",
            "rating",
            "description",
            "thumbnail",
            "gender",
            "imdb_id",
            "tmdb_id",
            "official_pages",
            "actor_tags",
            "ethnicity",
            "weight",
            "country_of_origin",
            "tattoos",
            "piercings",
            "height",
            "measurements",
            "extra_text",
            "tpdb_id",
            "last_lookup",
            "is_exempt_from_one_word_search",
            "actor_aliases",
            "scenes",
        ]

class ActorOutputSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='actor-detail')

    # alias = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='actor-alias-details-rest',
    #                                             lookup_field='actor-alias')

    # actor_aliases = ActorAliasSerializer()

    # actor_aliases = serializers.HyperlinkedRelatedField(allow_null=True, many=True, queryset=ActorAlias.objects.all(),
    #                                                     required=False, view_name='actor-alias-details-rest')

    # scenes = SceneIdNameSerializer(many=True, read_only=True)
    # actor_tags = ActorIdNameSerializer(many=True, read_only=True)

    actor_tags = ActorTagListSerializer(many=True, read_only=True)
    actor_aliases = ActorAliasSerializer(many=True, read_only=True)
    
    class Meta:
        model = Actor
        depth = 2
        fields = [
            "id",
            "name",
            "date_added",
            "date_fav",
            "date_runner_up",
            "date_of_birth",
            "play_count",
            "is_fav",
            "is_runner_up",
            "rating",
            "description",
            "thumbnail",
            "gender",
            "imdb_id",
            "tmdb_id",
            "official_pages",
            "actor_tags",
            "ethnicity",
            "weight",
            "country_of_origin",
            "tattoos",
            "piercings",
            "height",
            "measurements",
            "extra_text",
            "tpdb_id",
            "is_exempt_from_one_word_search",
            "actor_aliases",
        ]

        # exclude = ['actor_tags']
        # fields = ('url', 'name', 'actor_aliases', 'date_added')

        # Tutorial on http://www.django-rest-framework.org/tutorial/1-serialization/

        # pk = serializers.IntegerField(read_only=True)
        # name = serializers.CharField(max_length=50)
        # is_exempt_from_one_word_search = serializers.BooleanField(default=False)
        #
        # def create(self, validated_data):
        #     """
        #     Create and return a new `Snippet` instance, given the validated data.
        #     """
        #     return ActorAlias.objects.create(**validated_data)
        #
        # def update(self, instance, validated_data):
        #     """
        #     Update and return an existing `Snippet` instance, given the validated data.
        #     """
        #     instance.name = validated_data.get('name', instance.name)
        #     instance.is_exempt_from_one_word_search = validated_data.get('is_exempt_from_one_word_search',
        #                                                                  instance.is_exempt_from_one_word_search)
        #     instance.save()
        #     return instance


class SceneListSerializer(serializers.ModelSerializer):
    # actorss = ActorListSerializer(source='actors')

    actors = ActorIdNameMinimalSerializer(many=True, read_only=True)
    scene_tags = SceneIdNameSerializer(many=True, read_only=True)
    websites = WebsiteIdNameSerailzier(many=True, read_only=True)

    def setup_eager_loading(self, queryset):
        """Perform necessary eager loading of data.

        Args:
            queryset:
        """
        queryset = queryset.prefetch_related("actors", "scene_tags", "websites")
        return queryset

    class Meta:
        model = Scene
        # depth = 1
        # fields = ['id', 'name', 'path_to_file', 'path_to_dir', 'hash', 'date_added', 'date_fav', 'date_runner_up', 'play_count',
        #           'is_fav', 'is_runner_up', 'rating', 'description', 'thumbnail', 'scene_tags', 'actors', 'websites' ]
        fields = [
            "id",
            "name",
            "clean_title",
            "actors",
            "scene_tags",
            "websites",
            "thumbnail",
            "folders_in_tree",
            "is_runner_up",
            "rating",
            "path_to_file",
            "hash",
            "release_date",
        ]

        # fields = ['id', 'name']


class SceneSerializer(serializers.ModelSerializer):
    actors = ActorIdNameSerializer(many=True, read_only=True)
    scene_tags = SceneIdNameSerializer(many=True, read_only=True)
    websites = WebsiteIdNameSerailzier(many=True, read_only=True)

    class Meta:
        model = Scene

        # fields = ['id', 'name', 'path_to_file', 'path_to_dir', 'date_added', 'date_fav', 'date_runner_up', 'play_count',
        #           'is_fav', 'is_runner_up', 'rating', 'description', 'thumbnail', 'scene_tags', 'actors',
        #           'websites', 'width', 'height', 'bit_rate', 'duration', 'size', 'codec_name', 'framerate',
        #           'folders_in_tree']

        fields = [
            "id",
            "name",
            "clean_title",
            "path_to_file",
            "path_to_dir",
            "hash",
            "tpdb_id",
            "tpdb_scanned",
            "tpdb_scanned_match",
            "tpdb_scanned_unsure",
            "url",
            "release_id",
            "release_date",
            "date_added",
            "date_fav",
            "date_runner_up",
            "play_count",
            "is_fav",
            "is_runner_up",
            "rating",
            "thumbnail",
            "scene_tags",
            "actors",
            "websites",
            "width",
            "height",
            "bit_rate",
            "duration",
            "size",
            "codec_name",
            "framerate",
            "description",
            "folders_in_tree",
            "date_last_played",
            "orig_name",
            "orig_path_to_file",
        ]


class ActorTagSerializer(serializers.ModelSerializer):
    # actors = ActorIdNameSerializer(many=True, read_only=True)

    scene_tags = SceneTagIdNameSerialzier(many=True, read_only=True)

    class Meta:
        model = ActorTag
        # depth = 1
        fields = [
            "id",
            "name",
            "date_added",
            "date_fav",
            "date_runner_up",
            "play_count",
            "is_fav",
            "is_runner_up",
            "rating",
            "thumbnail",
            "actors",
            "scene_tags",
            "exclusions",
        ]


class PlaylistListSerializer(serializers.ModelSerializer):
    usage_count = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ["id", "name", "usage_count"]

    def get_usage_count(self, obj):
        """
        Args:
            obj:
        """
        return obj.scenes.count()


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = "__all__"
