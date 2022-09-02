# encoding=utf-8

from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class NoStrictManifestStaticFilesStorage(ManifestStaticFilesStorage):
    manifest_strict = False
