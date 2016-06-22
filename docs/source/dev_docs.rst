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

Resolving the "relation does not exist" error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you run a variation of the above command and encounter a traceback with this error message,

::

    django.db.utils.ProgrammingError: relation "streamwebs_site" does not exist
    LINE 1: ...ite"."created", "streamwebs_site"."modified" FROM "streamweb...
    
you probably have an unapplied migration from changes you made to a model
yourself, or changes someone else made to a model that got carried over from a
recent merge. To apply the migration and fix the error, run::

    python manage.py makemigrations
    python manage.py migrate

Then you can try to run your test command again. If you encounter this prompt,

::

    Got an error creating the test database: database "test_streamwebs" already exists
    Type 'yes' if you would like to try deleting the test database 'test_streamwebs', or 'no' to cancel: 

go ahead and type "yes". Your tests should then be able to run. 
