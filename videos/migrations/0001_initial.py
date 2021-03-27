# Generated by Django 3.1.6 on 2021-03-26 16:21

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_fav', models.DateTimeField(blank=True, null=True)),
                ('date_runner_up', models.DateTimeField(blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('play_count', models.IntegerField(default=0)),
                ('is_fav', models.BooleanField(default=False)),
                ('is_runner_up', models.BooleanField(default=False)),
                ('rating', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, default='')),
                ('thumbnail', models.CharField(blank=True, max_length=640, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('T', 'Transgender')], max_length=15)),
                ('imdb_id', models.CharField(blank=True, max_length=25, null=True)),
                ('tmdb_id', models.CharField(blank=True, max_length=25, null=True)),
                ('tpdb_id', models.CharField(blank=True, default='', max_length=48, null=True)),
                ('official_pages', models.TextField(blank=True, default='')),
                ('ethnicity', models.CharField(blank=True, max_length=30, null=True)),
                ('weight', models.CharField(blank=True, max_length=30, null=True)),
                ('country_of_origin', models.CharField(blank=True, max_length=30, null=True)),
                ('tattoos', models.CharField(blank=True, max_length=600, null=True)),
                ('piercings', models.CharField(blank=True, max_length=600, null=True)),
                ('height', models.CharField(blank=True, max_length=30, null=True)),
                ('measurements', models.CharField(blank=True, max_length=30, null=True)),
                ('extra_text', models.TextField(blank=True, default='')),
                ('last_lookup', models.DateTimeField(blank=True, null=True)),
                ('is_exempt_from_one_word_search', models.BooleanField(default=False)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActorAlias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('is_exempt_from_one_word_search', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LocalSceneFolders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SceneTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('play_count', models.IntegerField(default=0)),
                ('date_fav', models.DateTimeField(blank=True, null=True)),
                ('date_runner_up', models.DateTimeField(blank=True, null=True)),
                ('is_fav', models.BooleanField(default=False)),
                ('is_runner_up', models.BooleanField(default=False)),
                ('rating', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, default='')),
                ('thumbnail', models.CharField(blank=True, max_length=500, null=True)),
                ('scene_tag_alias', models.TextField(blank=True, default='')),
                ('exclusions', models.TextField(blank=True, default='', null=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('yapo_id', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('play_count', models.IntegerField(default=0)),
                ('date_fav', models.DateTimeField(blank=True, null=True)),
                ('date_runner_up', models.DateTimeField(blank=True, null=True)),
                ('is_fav', models.BooleanField(default=False)),
                ('is_runner_up', models.BooleanField(default=False)),
                ('rating', models.IntegerField(default=0)),
                ('thumbnail', models.CharField(blank=True, max_length=640, null=True)),
                ('website_alias', models.TextField(blank=True, default='')),
                ('exclusions', models.TextField(blank=True, default='', null=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('url', models.TextField(blank=True, default='', max_length=256, null=True)),
                ('tpdb_id', models.IntegerField(default=0)),
                ('filename_format', models.TextField(blank=True, default='', max_length=256, null=True)),
                ('scene_tags', models.ManyToManyField(blank=True, related_name='websites', to='videos.SceneTag')),
            ],
        ),
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('clean_title', models.CharField(blank=True, max_length=320, null=True)),
                ('tpdb_id', models.CharField(blank=True, default='', max_length=48, null=True)),
                ('tpdb_scanned', models.BooleanField(default=False)),
                ('tpdb_scanned_match', models.BooleanField(default=False)),
                ('tpdb_scanned_unsure', models.BooleanField(default=False)),
                ('url', models.CharField(blank=True, max_length=320, null=True)),
                ('release_id', models.CharField(blank=True, default='', max_length=64, null=True)),
                ('release_date', models.DateTimeField(blank=True, null=True)),
                ('hash', models.CharField(blank=True, default='', max_length=32)),
                ('path_to_file', models.CharField(max_length=640, unique=True)),
                ('path_to_dir', models.CharField(max_length=640)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_fav', models.DateTimeField(blank=True, null=True)),
                ('date_last_played', models.DateTimeField(blank=True, null=True)),
                ('date_runner_up', models.DateTimeField(blank=True, null=True)),
                ('last_filename_tag_lookup', models.DateTimeField(blank=True, null=True)),
                ('play_count', models.IntegerField(default=0)),
                ('is_fav', models.BooleanField(default=False)),
                ('is_runner_up', models.BooleanField(default=False)),
                ('rating', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, default='')),
                ('thumbnail', models.CharField(blank=True, max_length=500, null=True)),
                ('width', models.IntegerField(blank=True, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('bit_rate', models.IntegerField(blank=True, null=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('size', models.IntegerField(blank=True, null=True)),
                ('codec_name', models.CharField(blank=True, max_length=20, null=True)),
                ('framerate', models.FloatField(blank=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('orig_name', models.CharField(max_length=500, null=True)),
                ('orig_path_to_file', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('actors', models.ManyToManyField(blank=True, related_name='scenes', to='videos.Actor')),
                ('scene_tags', models.ManyToManyField(blank=True, related_name='scenes', to='videos.SceneTag')),
                ('websites', models.ManyToManyField(blank=True, related_name='scenes', to='videos.Website')),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('scenes', models.ManyToManyField(blank=True, related_name='playlists', to='videos.Scene')),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, unique=True)),
                ('last_folder_name_only', models.CharField(max_length=100, null=True)),
                ('path_with_ids', models.CharField(blank=True, max_length=900, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='videos.folder')),
                ('scenes', models.ManyToManyField(related_name='folders_in_tree', to='videos.Scene')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActorTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_fav', models.DateTimeField(blank=True, null=True)),
                ('date_runner_up', models.DateTimeField(blank=True, null=True)),
                ('play_count', models.IntegerField(default=0)),
                ('is_fav', models.BooleanField(default=False)),
                ('is_runner_up', models.BooleanField(default=False)),
                ('rating', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, default='')),
                ('thumbnail', models.CharField(blank=True, max_length=500, null=True)),
                ('actor_tag_alias', models.TextField(blank=True, default='')),
                ('exclusions', models.TextField(blank=True, default='', null=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('yapo_id', models.CharField(blank=True, max_length=32, null=True)),
                ('scene_tags', models.ManyToManyField(blank=True, related_name='actor_tags', to='videos.SceneTag')),
            ],
        ),
        migrations.AddField(
            model_name='actor',
            name='actor_aliases',
            field=models.ManyToManyField(blank=True, related_name='actors', to='videos.ActorAlias'),
        ),
        migrations.AddField(
            model_name='actor',
            name='actor_tags',
            field=models.ManyToManyField(blank=True, related_name='actors', to='videos.ActorTag'),
        ),
    ]
