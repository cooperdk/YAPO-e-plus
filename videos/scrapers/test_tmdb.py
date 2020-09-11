import os
from datetime import datetime

from django.db.models import Manager
from django.test import TestCase
import videos.models
from videos.scrapers import tmdb


class test_tmdb(TestCase):
    def createPersonInfo(self):
        return {
            'biography': None,
            'birthday': None,
            'also_known_as': [],
            'imdb_id': None,
            'id': None,
            'homepage': None,
            'gender': None,
            'profile_path' : None
        }

    def test_search_person_simple(self):
        # Do a lookup for this person, and make sure we get a match which populates gender.
        newActor = videos.models.Actor(name = 'Ava Addams')
        self.assertTrue(tmdb.search_person(newActor, None, False))
        actors = videos.models.Actor.objects.all()
        self.assertEqual(1, len(actors))
        self.assertEqual('F', actors[0].gender)

    def test_add_search_result_to_actor(self):
        newActor = videos.models.Actor(name = 'actorname')
        personInfo = self.createPersonInfo()
        personInfo['homepage'] = 'www.example.com'
        tmdb.add_search_results_to_actor(newActor, False, [personInfo])
        actors = videos.models.Actor.objects.all()
        self.assertEqual(1, len(actors))
        print(dir(actors[0]))
        print(actors[0].official_pages)
        self.assertEqual('www.example.com', actors[0].official_pages)

    def test_add_search_result_to_actor_akas(self):
        newActor = videos.models.Actor(name='actorname')
        personInfo = self.createPersonInfo()
        personInfo['also_known_as'] = ['akaname1', 'akaname2']
        tmdb.add_search_results_to_actor(newActor, False, [personInfo])
        actors = videos.models.Actor.objects.all()
        aliases = actors[0].actor_aliases.all()
        self.assertEqual(2, len(aliases))
        print("Aliases: %s" % aliases[0].name)
        self.assertEqual(1, len([x for x in aliases if x.name == 'akaname1']) )
        self.assertEqual(1, len([x for x in aliases if x.name == 'akaname2']) )

    def test_add_search_result_to_actor_clashing_akas(self):
        # These two actors both have the same alias - 'akanamecommon'.
        actor1 = videos.models.Actor(name='actor1')
        actor2 = videos.models.Actor(name='actor2')

        aka1 = self.createPersonInfo()
        aka1['also_known_as'] = ['akaname1', 'akanamecommon']

        aka2 = self.createPersonInfo()
        aka2['also_known_as'] = ['akaname2', 'akanamecommon']

        tmdb.add_search_results_to_actor(actor1, False, [aka1])
        tmdb.add_search_results_to_actor(actor2, False, [aka2])

        actor1res = videos.models.Actor.objects.get(name = 'actor1')
        actor2res = videos.models.Actor.objects.get(name = 'actor2')

        aka1res = actor1res.actor_aliases
        aka2res = actor2res.actor_aliases

        self.assertEqual(2, aka1res.count())
        self.assertEqual(2, aka2res.count())

        self.assertTrue(aka1res.get(name = 'akaname1'))
        self.assertTrue(aka1res.get(name = 'akanamecommon'))

        self.assertTrue(aka2res.get(name = 'akaname2'))
        self.assertTrue(aka2res.get(name = 'akanamecommon'))
