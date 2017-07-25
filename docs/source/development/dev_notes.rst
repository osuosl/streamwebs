.. _dev_notes:

===================
Miscellaneous Notes
===================

Resolving the "relation does not exist" error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you encounter the following error while running a variation of the above
command or while attempting to run the application in a browser,

::

    django.db.utils.ProgrammingError: relation "streamwebs_site" does not exist
    LINE 1: ...ite"."created", "streamwebs_site"."modified" FROM "streamweb...

you probably have an unapplied migration from changes you made to a model
yourself, or changes someone else made to a model that got carried over from a
recent merge. To apply the migration and fix the error, run::

    python manage.py makemigrations
    python manage.py migrate

Then you can try to run your command again. If you encounter this prompt while
testing,

::

    Got an error creating the test database: database "test_streamwebs" already exists
    Type 'yes' if you would like to try deleting the test database 'test_streamwebs', or 'no' to cancel:

go ahead and type "yes". Your tests should then be able to run. If they're not,
or you're trying to run the application and the original error wasn't resolved,
change directories into streamwebs_frontend/streamwebs/migrations and delete
all the migrations you find there (files that begin with a number and an
underscore). Afterwards you may have to run the makemigrations and migrate
commands again to generate an up-to-date migration that accurately represents
the current state of your models, but this should fix the problem. See the next
section for more details on how this project manages migrations.



Translation
-----------

In order to make a Django project translatable, you have to add a minimal number
of hooks to your Python code and templates. Django then provides utilities to
extract the translation strings into a message file. This file is a convenient
way for translators to provide the equivalent of the translation strings in the
target language. Once the translators have filled in the message file, it must
be compiled. Once this is done, Django takes care of translating Web apps on the
fly in each available language, according to users’ language preferences.
To enable i18n we need to make the following changes in the settings.py:

::

    from django.utils.translation import ugettext_lazy as _
    USE_I18N = True
    TEMPLATES = [
        {
            ...
            'OPTIONS': {
                'context_processors': [
                    ...
                    'django.template.context_processors.i18n',
                ],
            },
        },
    ]

::

    MIDDLEWARE_CLASSES = (
        ...
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        ...
    )

Note: the order is important!!!

Specify the languages you want to use:

::

    LANGUAGES = (
        ('en', 'English'),
        ('es', 'Español'),
    )

The ugettext_lazy function is used to mark the language names for translation,
and it’s usual to use the function’s shortcut _.
Note: there is another function, ugettext, used for translation.
The difference between these two functions is that ugettext translates the
string immediately whereas ugettext_lazy translates the string when rendering
a template.
All .py files containing text for translation should have

::

    from django.utils.translation import ugettext_lazy as _

towards the top of the file. Also settings.py should have local_paths specified

::

    LOCALE_PATHS = (
        '../locale/',
    )

The urls.py should contain this:

::

    url(r'^i18n/', include('django.conf.urls.i18n'))

Finally, mark the text you want to translate by wrapping it into _(' '), i.e.:
_('Password').

Template files have to contain

::

    {% load i18n %}

at the top and the text to be translated has to be wrapped around
{% ' ' %}, i.e.:

::

    {% 'Username:' %}

The string for translating Streamwebs website are extracted into
locale/.po files.
In docker run

::

    python manage.py makemessages -l <language code>

(i.e., 'python manage.py makemessages -l es' for Spanish). If this is a new
language just added into the settings.py, the command will create a new
directory in the locale folder with the .po file. If the language already
existed, the command will update the .po file.

After translating all the strings in .po file run

::

    python manage.py compilemessages

This runs over all available .po files and creates .mo files, which are binary files optimized for use by
gettext. For translators: use .po file of your working language, complete the space
in the empty parenthesis with the translations:

::

    #: streamwebs/templates/streamwebs/register.html:11
     msgid "Create an account."
     msgstr " "
