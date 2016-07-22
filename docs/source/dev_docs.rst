.. _dev_docs:

=======================
Developer Documentation
=======================
StreamWebs is built with the Django web framework. You can view and clone the
StreamWebs Github repository `here <https://github.com/osuosl/streamwebs>`_.

Testing
-------
The tests directory is located in streamwebs_frontend/streamwebs/ and contains
subdirectories (such as " models" and "views"), each of which contains files
that test individual models, views, etc. To run tests, you must be in the
same directory in which manage.py is located, i.e. /streamwebs_frontend/:

::

    python manage.py test streamwebs/tests/<subdirectory>/

For example,

::

    python manage.py test streamwebs/tests/models/

would run all the model tests. You can find a thorough explanation of how the
Django testing framework works in its `official documentation
<https://docs.djangoproject.com/en/1.8/topics/testing/overview/#running-tests>`_.

.. _error:

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

Handling Migrations
-------------------
This project currently does not track migrations on GitHub. As Django models
are developed, they go through many changes and thus generate many migrations.
Since this is a team project with multiple developers responsible for the
creation of multiple models, these migrations can conflict with each other upon
merges. To avoid this inconvenience, we have decided not to track migrations on
Github by deleting them on our own branches prior to making pull requests. The
only file in the repository's streamwebs_frontend/streamwebs/migrations should
be an __init__.py file. For an example of how keeping migrations can cause
problems during development, see the previous section on :ref:`error`. You can
also read `this Stack Overflow discussion
<http://stackoverflow.com/questions/28035119/should-i-be-adding-the-django-migration-files-in-the-gitignore-file>`_
that shares the insights and experiences of other developers concerning
migrations and version control.

Translation
-------------------

The string for translating Streamwebs website are extracted into locale/.po files.
In order to include a new language, go to settings and add your language code.
In docker run 'python manage.py makemessages -l <language code>'
(i.e., 'python manage.py makemessages -l es' for Spanish). After translating all
the strings in .po file 'run python manage.py compilemessages'.
