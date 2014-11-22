from django.test import TestCase
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django_gcs.storage import GoogleCloudStorage

class TestStorage(TestCase):
    def setUp(self):
        self.storage = default_storage

    def tearDown(self):
        pass

    def test_exist(self):
        cf = ContentFile('some content')
        path = self.storage.save('test.txt', cf)




