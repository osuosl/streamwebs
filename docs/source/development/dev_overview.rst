.. _dev_overview:

===============
Project Outline
===============

Streamwebs is an education science platform for educators and students in
Oregon's public schools. The application allows students to enter data about
streams and wetlands gathered on field trips, then graph or export the data for
further analysis.

This application is a re-write of the original Drupal-based Streamwebs
application. Until the new application goes live, the original can be found at
`http://streamwebs.org`_.


Core Components
---------------

Streamwebs is written in Python usign the `Django`_ web framework. It follows
Python's PEP8 coding style and standard Django MVC structure. Streamwebs also
makes use of geographic information and the Google Maps API. The underlying data
store is Postgres with geographic data extensions (PostGIS).

Streamwebs also uses the D3 javascript library for generating graphs, and the
Materialize CSS framework for the front-end UI elements.

Sites
=====

The Primary object in Streamwebs is the Site, which consists of a name,
description, location (coordinates), and optionally an image. Site locations are
point objects and are displayed in a map view as markers. All data is associated
with a site, and the site view is the starting point for entering, viewing,
graphing or downloading collected data.

Datasheets
==========

Datasheets are associated with a site, and with a school, they store collected
data about a stream - air temperature, water temperature, species detected, etc.
There are six datasheets currently defined:

- Canopy Cover: records percentage of the sky obscured by forest canopy
- Macroinvertibrates: records the numbers of specific species of invertebrates
- Photo Point: records images taken at a specific location Riparian Transect:
- records species in a cross-section of a streambed Soil Survey: records the
- types of soil found Water Quality: records various water measurments such as
- temperature and oxygen level

Each datasheet has its own model, form, view and database table, and may have
associated models, for example mulitple samples for a specific measurement.

Datasheet views are designed to resemble as closely as possible the paper
versions that are taken into the field to record data. Calculated values are
automatically calculated on data entry. PDF files for each sheet are provided
for printing.

Users
=====

Students and teachers share a general 'user' role. Users are authorized to enter
data and create sites, the only reserved permissions are file uploads and
viewing site statistics.

Users are associated with a School. Birth date is a required field for account
creation, and students must be 13 years of age or older to sign up.

Users can self-register, by default they will be placed in the general user
role, a admin can promote any user to an admin role. The initial admin account
is the Django 'superadmin', created on deployment, and this superadmin should
designate one or more user accounts as admins.

Resources
=========

Several types of files are available for download from the site. A generic
'resource' model is used to store datasheets, educator kits, publications and
tutorial videos, and these resources are displayed on type-specific pages. An
index of all resources is located at /resources.

Statistics
==========

Basic site statistics are available to admin users. Number of users, site and
datasheets are the primary statistics.

Schools
=======

A model containing a list of known public schools in Oregon, used for tracking
which school contributed data to a site. Also associated with users.

.. note::

  Data is associeted explicitly with a school, we do not rely on the account of
  the user who entered data for determining which school created the data.

Test Suite
==========

All views, forms, permissions and models are tested with unit tests. These tests
use the Django test framework.

Internationalization
====================

Streamwebs uses Django's translations framework to translate strings into
supported languages.

Dev Environment
===============

The Streamwebs project uses Docker and docker-compose for running test and a
local instances of the application for development purposes.

The ``docker-compose.yml`` will build a postgres database container with the
necessary PostGIS extensions, and a 'web' container running the application.
Standard docker commands can be used to run the test suite or other management
commands in the web container.

Data Import
===========

On initial deployment, the application will be seeded with data exported from
the old Drupal application. A number of scripts in the ``data_scripts``
directory are responsible for importing data. These scripts will be run by the
deployment script, and should only be run once per application instance. Due to
the complexity of the Drupal exported data, modifying this code is not
recommended.

User accounts will be imported from the previous application, and ever active
member will be sent an email explaining how to reset their password for the new
system.
