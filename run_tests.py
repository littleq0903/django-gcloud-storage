import sys
import os

from optparse import OptionParser

from django.conf import settings

project_root = os.path.dirname(os.path.abspath(__file__))

try:
    test_settings = {
        'DEBUG': True,

        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3'
            }
        },

        'INSTALLED_APPS': [
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites"
        ],

        'SITE_ID': 1,
        'NOSE_ARGS': ['-s'],
        'DEFAULT_FILE_STORAGE': 'django_gcs.storage.GoogleCloudStorage',

        'CACHES': {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            }
        }
    }

except ImportError:
    raise ImportError('run `pip install -r requirements_test.txt to install testing dependencies.')

try:
    import test_secrets

    gcs_settings = {
        'DJANGO_GCS_PROJECT': test_secrets.DJANGO_GCS_PROJECT,
        'DJANGO_GCS_CLIENT_EMAIL': test_secrets.DJANGO_GCS_CLIENT_EMAIL,
        'DJANGO_GCS_PRIVATE_KEY_PATH': test_secrets.DJANGO_GCS_PRIVATE_KEY_PATH,
        'DJANGO_GCS_BUCKET': test_secrets.DJANGO_GCS_BUCKET
    }

except ImportError:

    if 'DJANGO_GCS_PROJECT' not in os.environ:
        raise Exception('please provide Google Cloud Credentials in eithor environment vars or test_secrets.py')

    gcs_settings = {
        'DJANGO_GCS_PROJECT': os.environ['DJANGO_GCS_PROJECT'],
        'DJANGO_GCS_CLIENT_EMAIL': os.environ['DJANGO_GCS_PROJECT'],
        'DJANGO_GCS_PRIVATE_KEY_PATH': os.environ['DJANGO_GCS_PROJECT'],
        'DJANGO_GCS_BUCKET': os.environ['DJANGO_GCS_PROJECT']
    }


all_settings = {}
all_settings.update(test_settings)
all_settings.update(gcs_settings)

settings.configure(**all_settings)

import django
django.setup()

from django_nose import NoseTestSuiteRunner

def run_tests(*args):
    if not args:
        args = ['tests']

    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(args)

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    run_tests(*args)
