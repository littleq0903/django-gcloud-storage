from django.core.files.storage import Storageo
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

from gcloud import storage as gc_storage

class GoogleCloudStorage(Storage):
    def __init__(self, project=None, client_email=None, private_key_path=None):
        self.project = project if project else settings.DJANGO_GCS_PROJECT
        self.client_email = client_email if client_email else settings.DJANGO_GCS_CLIENT_EMAIL
        self.private_key_path = private_key_path if private_key_path else settings.DJANGO_GCS_PRIVATE_KEY_PATH

        self.bucket = gc_storage.get_bucket(
                project=self.project, client_email=self.client_email, private_key_path=self.private_key_path)

    def path(self, name):
        return name

    def _open(self, name, mode='rb'):
        gc_file = self.bucket.get_key(self.path(name))

        return gc_file.get_contents_as_string()

    def _save(self, name, content):
        gc_file = self.bucket.get_key(self.path(name))
        gc_file.set_contents_as_string(content)

