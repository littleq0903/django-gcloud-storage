from django.db import models

TEST_FOLDER_NAME = "gcs-unittest"

class TestModel(models.Model):
    text = models.CharField(max_length=10)
    text_file = models.FileField(upload_to=TEST_FOLDER_NAME)
    image_file = models.ImageField(upload_to=TEST_FOLDER_NAME)

    def __unicode__(self):
        return self.text
