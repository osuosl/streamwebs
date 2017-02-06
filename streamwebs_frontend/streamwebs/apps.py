from __future__ import unicode_literals

from django.apps import AppConfig


class StreamwebsConfig(AppConfig):
    name = 'streamwebs'

    def ready(self):
        import signals  # NOQA
