from django.test import TestCase
import videos.models
from videos.scrapers import freeones


class test_freeones(TestCase):
    def test_add_search_result_to_actor_clashing_akas(self):
        # These two actors both have the same alias - 'akanamecommon'.
        actor1 = videos.models.Actor(name='actor1')
        actor2 = videos.models.Actor(name='actor2')

        actor1.save()
        actor2.save()

        freeones.insert_aliases(actor1, 'akaname1, akanamecommon')
        freeones.insert_aliases(actor2, 'akaname2, akanamecommon')

        actor1.save()
        actor2.save()

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
