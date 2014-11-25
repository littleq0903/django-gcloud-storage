from django.test import TestCase
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.core.files.storage import default_storage

from django_gcs.storage import GoogleCloudStorage

from test_app.models import TestModel

class TestStorage(TestCase):
    def setUp(self):
        self.storage = default_storage

        self.test_bucket_name = 'django-gcs-testing'
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
        self.test_img_path = 'misc/img/django_logo.png'
        self.test_txt_path = 'misc/txt/python-zen.txt'

        # create a new bucket for testing purpose
        self.test_connection = self.storage.gc_connection
        self.test_bucket = self.storage.gc_bucket

        # upload a fake data for checking download functionality
        self.existed_file = self.test_bucket.new_key(self.test_existed_file_name)
        self.existed_file.upload_from_string(self.test_existed_file_content)

    def tearDown(self):
        # perform a clean up for restoring cloud storage
        all_keys = self.test_bucket.get_all_keys()

        keys_to_del = filter(lambda k: k.name.startswith("%s/" % self.test_folder_name), all_keys)
#        map(lambda k: k.delete(), keys_to_del)


    def test_save(self):
        # save multiple files
        for i in range(2):
            cf = ContentFile('some content')
            new_name = self.storage.save('%s/test.txt' % self.test_folder_name, cf)

            # perform checking
            new_key = self.test_bucket.get_key(new_name)
            self.assertTrue(new_key.exists())


    def test_open(self):
        downloaded_file = self.storage.open(self.test_existed_file_name, 'r')

        self.assertEqual(downloaded_file.read(), self.test_existed_file_content)


    def test_url(self):
        right_public_url = self.test_bucket.get_key(self.test_existed_file_name).public_url
        test_public_url = self.storage.url(self.test_existed_file_name)

        self.assertEqual(right_public_url, test_public_url)


    def test_size(self):
        right_file_size = self.test_bucket.get_key(self.test_existed_file_name).size
        test_file_size = self.storage.size(self.test_existed_file_name)

        self.assertEqual(right_file_size, test_file_size)


    def test_listdir(self):
        def new_content(key):
            new_key = self.test_bucket.new_key( "%s/%s" % (self.test_folder_name, key))
            new_key.upload_from_string('testing content')

        # upload structural data
        new_content('a1/b1/1.txt')
        new_content('a1/b2/1.txt')
        new_content('a1/1.txt')
        new_content('a1/2.txt')

        dirs, files = self.storage.listdir('%s/a1' % self.test_folder_name)

        self.assertEquals(set(dirs), set([u"b1", u"b2"]))
        self.assertEquals(set(files), set([u"1.txt", u"2.txt"]))


    def test_filefield(self):

        test_model_instance = TestModel.objects.create()
        test_model_instance.image_file = ImageFile(open(self.test_img_path))
        test_model_instance.text_file = ContentFile(open(self.test_txt_path))
        test_model_instance.save()

        # TODO: verify upload of both image and text files
        
