from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

from gcloud import storage as gc_storage

class GoogleCloudStorage(Storage):
    def __init__(self, bucket_name=None, project=None, client_email=None, private_key_path=None):
        self.bucket_name = bucket_name if bucket_name else settings.DJANGO_GCS_BUCKET
        self.project = project if project else settings.DJANGO_GCS_PROJECT
        self.client_email = client_email if client_email else settings.DJANGO_GCS_CLIENT_EMAIL
        self.private_key_path = private_key_path if private_key_path else settings.DJANGO_GCS_PRIVATE_KEY_PATH

        self.__gc_connection = gc_storage.get_connection(self.project, self.client_email, self.private_key_path)
        self.bucket = self.__gc_connection.get_bucket(self.bucket_name)


    def path(self, name):
        return name


    def _open(self, name, mode='rb'):
        gc_file = self.bucket.get_key(self.path(name))

        return gc_file.get_contents_as_string()


    def _save(self, name, content):
        gc_file = self.bucket.get_key(self.path(name))

        gc_file.set_contents_as_string(content)

   
    def delete(self, name):
        gc_file = self.bucket.get_key(self.path(name))

        gc_file.delete()


    def exists(self, name):
        gc_file = self.bucket.get_key(self.path(name))

        return gc_file.exists()

