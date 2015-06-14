from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test.testcases import TestCase
from core.models import Entry, Log

__author__ = 'alexandreferreira'


class EntryTest(TestCase):

    def test_create(self):
        entry = Entry.objects.create(1, u"Alex")
        self.assertEqual(entry.number, 1)
        self.assertEqual(entry.text, "Alex")

    def test_create_error_number(self):
        with self.assertRaises(ValueError):
            Entry.objects.create("a", u"Alex")

    def test_delete(self):
        entry = Entry.objects.create(1, u"Alex")
        entry.delete()
        exists = Entry.objects.filter(number=1).exists()
        self.assertFalse(exists)

    def test_view_list(self):
        entry = Entry.objects.create(1, u"Alex")
        entry2 = Entry.objects.create(2, u"Isabel")
        client = Client()
        url = reverse('entry_list')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        entries = response.context_data['entries']
        self.assertEqual(len(entries), 2)
        self.assertEqual(entry, entries[0])
        self.assertEqual(entry2, entries[1])

    def test_view_create(self):
        client = Client()
        url = reverse('entry_create')

        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        response = client.post(url, data={'number': 1, 'text': u'Alex'})
        self.assertEqual(response.status_code, 302)

        self.assertTrue(Entry.objects.filter(number=1).exists())

    def test_view_update(self):
        entry = Entry.objects.create(1, u"Alex")

        client = Client()
        url = reverse('entry_update', args=(1, ))
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        entry_response = response.context_data['entry']
        self.assertEqual(entry, entry_response)
        self.assertIn('form', response.context_data)

        url = reverse('entry_update', args=(1, ))
        response = client.post(url, data={'number': 1, 'name': u"Marcelo"})
        self.assertEqual(response.status_code, 200)
        entry_response = response.context_data['entry']
        self.assertEqual(entry, entry_response)
        self.assertIn('form', response.context_data)

    def test_view_delete(self):
        entry = Entry.objects.create(1, u"Alex")

        client = Client()
        url = reverse('entry_delete', args=(1, ))
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        entry_response = response.context_data['entry']
        self.assertEqual(entry, entry_response)

        url = reverse('entry_delete', args={1, })
        response = client.post(url)
        self.assertEqual(response.status_code, 302)

        exists = Entry.objects.filter(number=1).exists()
        self.assertFalse(exists)


class LogTest(TestCase):

    def test_register_create_entry(self):
        entry = Entry.objects.create(1, u"Alex")
        Log.objects.register_create_entry(entry.number, entry.text)
        exists = Log.objects.filter(entry=entry, log_type=Log.CREATE).exists()
        self.assertTrue(exists)

    def test_register_update_entry(self):
        entry = Entry.objects.create(1, u"Alex")
        Log.objects.register_edit_entry(entry.number, entry.text)
        exists = Log.objects.filter(entry=entry, log_type=Log.EDIT).exists()
        self.assertTrue(exists)

    def test_register_view_entry(self):
        entry = Entry.objects.create(1, u"Alex")
        Log.objects.register_view_entry(entry.number, entry.text)
        exists = Log.objects.filter(entry=entry, log_type=Log.VIEW).exists()
        self.assertTrue(exists)

    def test_register_delete_entry(self):
        entry = Entry.objects.create(1, u"Alex")
        Log.objects.register_delete_entry(entry.number, entry.text)
        exists = Log.objects.filter(entry=entry, log_type=Log.DELETE).exists()
        self.assertTrue(exists)
