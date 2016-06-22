.. _dev_docs: 

=======================
Developer Documentation
=======================
StreamWebs is built with the Django web framework. You can view and clone the StreamWebs Github repository `here <https://github.com/osuosl/streamwebs>`_. 

Testing
-------
The tests directory is located in streamwebs_frontend/streamwebs/ and contains three subdirectories: forms, models, and views, each of which contains files that test individual forms, models, and views. To run tests, you must be in the same directory in which manage.py is located, i.e. /streamwebs_frontend/:

::

    python manage.py test streamwebs/tests/<subdirectory>/

For example,::

    python manage.py test streamwebs/tests/models/

would run all the model tests. You can find a thorough explanation of how the Django testing framework works in its `official documentation <https://docs.djangoproject.com/en/1.8/topics/testing/overview/#running-tests>`_. 

Common testing issues and how to resolve them
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


