from django.test import TestCase
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django_gcs.storage import GoogleCloudStorage

class TestStorage(TestCase):
    def setUp(self):
        self.storage = default_storage

        self.test_folder_name = 'gcs-unittest'
        self.test_existed_file_name = '%s/gcs-existed.txt' % self.test_folder_name
        self.test_existed_file_content = """The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!"""

        # perform a clean up to testing folder
        self.test_bucket = self.storage.bucket
        try:
            self.test_bucket.delete_key(self.test_folder_name)
        except:
            pass

        # upload a fake data for checking download functionality
        self.existed_file = self.test_bucket.new_key(self.test_existed_file_name)
        self.existed_file.upload_from_string(self.test_existed_file_content)

    def tearDown(self):
        pass

    def test_save(self):
        # save multiple files
        for i in range(2):
            cf = ContentFile('some content')
            new_name = self.storage.save('%s/test.txt' % self.test_folder_name, cf)

            # perform checking
            new_key = self.test_bucket.get_key(new_name)
            assert new_key.exists()

    def test_open(self):
        downloaded_file = self.storage.open(self.test_existed_file_name, 'r')

        assert downloaded_file.read() == self.test_existed_file_content

        
        





