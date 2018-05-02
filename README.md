# django-gcloud-storage 

Build status: [![Build Status](https://travis-ci.org/littleq0903/django-gcloud-storage.svg?branch=master)](https://travis-ci.org/littleq0903/django-gcloud-storage)

Django Storage Backend on Google Cloud Storage with gcloud-python.

This storage backend allows you to store your static content to Google Cloud Storage in your Django app, by using the latest python wrapper from Google, `gcloud-python`.

---

## Setup

Currently you have to install it manually due to active development, I haven't publish it onto pip yet.

```shell
git clone https://github.com/littleq0903/django-gcloud-storage.git
cd django-gcloud-storage
pip install -r requirements.txt
pip install .
```

## Install to Your Django App

To enable this as your default file storage backend, you have to specify **django_gcs** as your default storage backend.

```python
# .../settings.py

...

DEFAULT_FILE_STORAGE = 'django_gcs.storage.GoogleCloudStorage'

```

Then you're all set, Django will start storing static content into Google Cloud Storage instead of local storage.

---

## Development

Disclaimer: This is project is under very first stage and active development, feedback and PRs are welcome.

## Arthors

* [Colin Su](http://github.com/littleq0903)
