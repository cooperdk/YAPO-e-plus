from django.test import TestCase
import videos.models
from videos.scrapers.scanner_tpdb import scanner_tpdb

class Testscanner_tpdb(TestCase):
    def test_resolve_performer_simple(self):
        uut = scanner_tpdb()

        # Make some actors
        for newname in ('twilight', 'spike', 'discord'):
            videos.models.Actor(name=newname).save()

        # Try to look one of them up.
        self.assertIsNotNone(uut.resolvePerformer({ 'name': 'spike' }))

    def test_resolve_performer_aliases(self):
        uut = scanner_tpdb()

        # Make some actors, with aliases
        for newname in ('twilight', 'spike', 'discord'):
            actor = videos.models.Actor(name=newname)
            actor.save()
            actor.createOrAddAlias("%s_alias" % newname)
            actor.save()

        # Try to look one of them up by an alias.
        found = uut.resolvePerformer({'name': 'spike_alias'})
        self.assertIsNotNone(found)
        self.assertEqual('spike', found)