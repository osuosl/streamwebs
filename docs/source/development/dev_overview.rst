.. _dev_overview:

========
Overview
========

Streamwebs is an science education platform for educators and students in
Oregon's public schools. The application allows students to enter data about
streams and wetlands gathered on field trips, then graph or export the data for
further analysis.

This application is a re-write of the original Drupal-based Streamwebs
application. Until the new application goes live, the original can be found at
`Streamwebs.org`_.

.. _`Streamwebs.org`: http://streamwebs.org

Core Components
---------------

Streamwebs is written in Python usign the `Django`_ web framework. It follows
Python's PEP8 coding style and standard Django MVC structure. Streamwebs also
makes use of geographic information and the Google Maps API. The underlying data
store is Postgres with geographic data extensions (PostGIS).

Streamwebs also uses the D3 javascript library for generating graphs, and the
Materialize CSS framework for the front-end UI elements.

.. _`Django`: https://docs.djangoproject.com/en/1.11/


Django Structure
================

Django's MVC model is slightly odd, what would normally be called a Controller
is a View, and what would be called a View is a Template. Models are what you
would expect, a description of the data model, for use with Django's ORM. URLs
are defined in a separate file.

Models
------

All models are defined in ``streamwebs_frontend/streamwebs/models.py``

Views
-----

Views are typically divided logically into several files according to the model
they refer to. Streamwebs doesn't do this, all general views are defined in
``streamwebs_frontend/streamwebs/views/general.py``, and a separate set of
views specifically dealing with CSV export are in
``streamwebs_frontend/streamwebs/views/export.py``

Views recieve the current http request object object and returns an HTTP
response object. See `Django Request and response objects`_ for their structure.

Views may also be 'decorated' to restrict access to logged in users. See
`Django View Decorators`_ for information on what can be done with decorators.

For example, you will see this construction frequently in the views file:

::

  @login_required
  def create_site(request):
      created = False
      ...

The `@login_required` is a decorator provided by the
`Django Authentication Framework`_ and prevents non-authenticated users from
accessing this view.

.. _`Django Authentication Framework`: https://docs.djangoproject.com/en/1.11/topics/auth/

.. _`Django View Decorators`: https://docs.djangoproject.com/en/1.11/topics/http/decorators/

.. _`Django Request and response objects`: https://docs.djangoproject.com/en/1.11/ref/request-response/


Templates and TemplateTags
--------------------------

Django by default uses a template language similar to Jinja2,  other backends
can be defined, but Streamwebs sticks to the default. Templates have the
`.html` extension and are found in ``streamwebs_frontend/streamwebs/templates/``

Templates have an inheritance structure, our base template sets up the HTML
page, and other templates inherit this structure. See `Django Templates`_ for
more information.

Streamwebs also makes use of TemplateTags, which can be used to transform text
in templates. These are defined in
``streamwebs_frontend/streamwebs/templatetags/filters.py``.
See `Custom Django Template Tags`_ for more information.

In templates, filters are included using ``{% load filters %}`` at the topof
the file. A filter is applied with the ``|`` character appended to a rendered
template variable:

::

  {{ 'zone'|get_zone_labels }}

.. _`Custom Django Template Tags`: https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/

.. _`Django Templates`: https://docs.djangoproject.com/en/1.11/topics/templates/


URLs
----

Streamwebs defines its URLs in ``streamwebs_frontend/streamwebs/urls.py``.

This file defines all URLs and connects them to their view method, which should
then render the appropriate template.

URLs are namespaced, the ``app_name = 'streamwebs'`` line ensures that URLs are
relative to the ``streamwebs`` app. In practicat terms, the important thing to
know is that links in templates are specified with the streamwebs namespace:

::

  {% url 'streamwebs:register' %}

This contruction will render the URL named ``register`` in the ``streamwebs``
application.

Sites
=====

The Primary object in Streamwebs is the Site, which consists of a name,
description, location (coordinates), and optionally an image. Site locations are
point objects and are displayed in a map view as markers.

All data is associated with a site, and the site view is the starting point for
entering, viewing, graphing or downloading collected data.

See :ref:`Sites <dev_sites>` for more details.

Datasheets
==========

Datasheets are associated with a site, and also with a school. They store
collected data about a stream - air temperature, water temperature, species
detected, etc.

There are six datasheets currently defined:

- Canopy Cover: records percentage of the sky obscured by forest canopy
- Macroinvertibrates: records the numbers of specific species of invertebrates
- Photo Point: records images taken at a specific location
- Riparian Transect: records plant types in a cross-section of a streambed
- Soil Survey: records the types of soil found
- Water Quality: records various water measurments such as temperature and
  oxygen level

Each datasheet has its own model, form, view and database table, and may have
associated models, for example mulitple samples for a specific measurement.

Datasheet views are designed to resemble as closely as possible the paper
versions that are taken into the field to record data. Calculated values are
automatically calculated on data entry. PDF files for each sheet are provided
for printing.

See :ref:`Datasheets <dev_datasheets>` for more details.

Graphing
========

See :ref:`Graphing <dev_graphs>` for more details.

Users
=====

Students and teachers share a general 'user' role. Users are authorized to enter
data and create sites, the only reserved permissions are resource file uploads
and viewing site statistics.

Users are associated with a School. Birth date is a required field for account
creation, and students must be 13 years of age or older to sign up.

Users can self-register, by default they will be placed in the general user
role, a admin can promote any user to an admin role. The initial admin account
is the Django 'superadmin', created on deployment, and this superadmin should
designate one or more user accounts as admins.

See :ref:`Users <dev_users>` for more details.

Resources
=========

Several types of files are available for download from the site. A generic
'resource' model is used to store datasheets, educator kits, publications and
tutorial videos, and these resources are displayed on type-specific pages. An
index of all resources is located at /resources.

See :ref:`Resources <dev_resources>` for more details.

Statistics
==========

Basic site statistics are available to admin users. Number of users, site and
datasheets are the primary statistics.

See :ref:`Statistics <dev_stats>` for more details.

Schools
=======

A model containing a list of known public schools in Oregon, used for tracking
which school contributed data to a site. Also associated with users.

.. note::

  Data is associeted explicitly with a school, we do not rely on the account of
  the user who entered data for determining which school created the data.

See :ref:`Schools <dev_schools>` for more details.


Test Suite
==========

All views, forms, permissions and models are tested with unit tests. These tests
use the Django test framework.

In addition to tests, files should be analyzed by the Flake8 python linter,
which enforces Python standard PEP8.

Development of new features should begin with writing a test for that feature.

See :ref:`Tests <tests>` for more details.

Internationalization
====================

Streamwebs uses the `Django translation framework`_ to translate strings into
supported languages. Supported languages can be selected using a pull-down
selector in the application.

Supported languages are set using the ``LANGUAGES`` setting. The default
application application language is set in ``LANGUAGE_CODE`` and defaults to
``en-us``.

Translation in the templates is done using the ``trans`` template tag, and in
python code by the _() method. Translations of these strings are stored in
message files, which contain string identifiers (typically just the original
string in the default application language) and that strings translation into
the target language.

To create a new messages file for language ``<lang>`` use the command

::

  django-admin makemessages -l <lang>

This will extract translatable strings from the code (strings in a ``trans``
tag or ``_()`` method) and write them to a message file:

``locale/<lang>/LC_MESSAGES/django.po``

See the `Django translation framework`_  documentation for much more
information about the translation framework.

See :ref:`Translation <translations>` for more details about translation
implementation in Streamwebs.


.. _`Django translation framework`: https://docs.djangoproject.com/en/1.11/topics/i18n/translation/


Data Import
===========

On initial deployment, the application will be seeded with data exported from
the old Drupal application. A number of scripts in the ``data_scripts``
directory are responsible for importing data. These scripts will be run by the
deployment script, and should only be run once per application instance. Due to
the complexity of the Drupal exported data, modifying this code is not
recommended.

User accounts will be imported from the previous application, and when the
production instance is ready, every active member will be sent an email
explaining how to reset their password for the new system.

See :ref:`Data Import <data_import>` for more details.

Dev Environment
===============

The Streamwebs project uses Docker and docker-compose for running test and a
local instances of the application for development purposes.

The configuration in ``docker-compose.yml`` will build a postgres database
container with the necessary PostGIS extensions, and a 'web' container running
the application.

Standard docker commands can be used to run the test suite or other management
commands in the web container.

See the contents of ``dockerfiles/`` for the Docker container definition and
startup/cleanup scripts.

Setup and configuration
~~~~~~~~~~~~~~~~~~~~~~~

First, make sure you have a working Docker install, the Docker daemon is
running, and your user has permission to run Docker.

Second, make sure you have the python package docker-compose installed. The
easiest way to do this is to create a local python virtualenv and install
docker-compose into that.

::

  virtualenv venv
  source venv/bin/activate
  pip install docker-compose

.. note:

  It will probably be useful to also install ``sphinx`` for building
  documentation. It's optional, but sometimes useful, to also install all of the
  application's requirements as well, with ``pip install -r requirements.txt``

Finally, configure the application. Streamwebs ships with some default settings
in several 'dist' files. These files need to be copied to their proper names
before the application will run.

These files may be edited, but should be adequate as-is for the Docker dev
environment.

The main application settings:

::

  cp streamwebs_frontend/streamwebs_frontend/settings.py.dist \
  /streamwebs_frontend/streamwebs_frontend/settings.py

The docker environment:

::

  cp dockerfiles/Dockerfile.env.dist dockerfiles/Dockerfile.env


Running the Dev Docker Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When ``docker-compose`` is installed and setttings are in place, you can launch
the dev environment with:

::

  docker-compose up web

This will build the PostGis container and a new CentOS container with the
streamwebs application running on port 8000. You should see the application at
``http://localhost:8000``.

Running management commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run management command in the docker environment, or to import data, you can
run a bash shell in the container:

::

  docker-compose run web bash

**Migrating the database**

The database schema is managed by migration files in
``streamwebs_frontend/streamwebs/migrations``.

If this is the first time you've built the docker PostGis container, you will
need to migrate the fresh database with the initial migration:

::

  docker-compose run web bash
  cd streamwebs_frontend/streamwebs_frontend
  ./manage.py migrate

Any changes to the schema should be expressed in a new migration. These can be
written manually, but it is much easier and safer to let Django generate them
based on changes to the models code.

After making changes to models that effect the schema, make new migrations:

::

  docker-compose run web bash
  cd streamwebs_frontend
  ./manage.py makemigrations

And migrate to update the schema:

::

  docker-compose run web bash
  cd streamwebs_frontend
  ./manage.py migrate

**Importing Data**

Data import scripts are idempotent, they load their data from CSV files in the
``csvs`` directory. The ``get_all.sh`` shell script will run all
of the python data import scripts in the correct order. The database should be
migrated prior to importing data.

::

  docker-compose run web bash
  cd data_scripts
  ./get_all

You can also import individual data types using the python scripts in this
directory.

**Creating a superuser**

To create a superuser (site admin account with all permissions):

::

  docker-compose run web bash
  cd streamwebs_frontend
  ./manage.py createsuperuser

The script will ask for a name, password and email address.

**Run a database shell**

Django provides a convenient console to the database, saving you the time of
manually connecting:

::

  docker-compose run web bash
  cd streamwebs_frontend
  ./manage.py dbshell

This will place you at a the psql commandline for the streamwebs Postgres
database running in the PostGis container. Type ``help`` for a listing of psql
commands, or ``\d`` to see Streamwebs' tables.
