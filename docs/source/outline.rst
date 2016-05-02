.. _project_outline:

===============
Project Outline
===============

Current plan for the StreamWebs rewrite. For a rough visual representation, 
refer to `this`_.

For now, the site's homepage will be a static intro that contains a brief
description about what StreamWebs is. Make sure the page is editable for
later renditions of the site.

From ``Home``, the user will be able to navigate to one of the
following pages:

* Create Account/Login
* Sites
* Resources

.. note::

    There are several things that may later be added to the site, so keep the
    following in mind while working on the build/structure of StreamWebs:
    
    * A built-in internationalization template (for multiple languages)
    * Methods for reporting/tracking user activity
    * A database table containing school names - so that a user can select
      from a list of schools when creating a new account

.. _this: http://i.imgur.com/XqOmLQn.jpg


Create Account/Login
--------------------

After login, the user will be taken to the central ``Sites`` page.

.. note::

    Alongside **Users**, basic CRUD will need to be implemented for
    **Resources** and **Map/Sites** as well.

Resources
---------

``Resources`` will contain all of StreamWebs' data sheets along with
external/internal links to supplementary information and the curriculum. Make
sure this page is editable through the admin panel as well.

Sites
-----

**Default Display**

The user will be able to navigate to a specific site in one of three ways:

  #) By name
  #) Via location marker on the map
  #) Through a pull down menu

Modes 1 and 3 are self-explanatory. Here's how the 2nd option will work:

The center of the sites page will contain a map display with markers denoting
site locations. Selecting a marker on the map will display additional info
about the site in a pop-up (for now, this will be the site name and a small
image). The user should be able to navigate to the selected site's page by
clicking on the view button displayed in the pop-up.

For a rough visual representation on how the default display will look, refer
to ``sites_default_041116.jpg`` in the ``_static`` directory. 

.. note::

    Map pin size for each site will vary depending on the number of data sheets
    inputted for that location.

**If Authenticated**

If the user has been authenticated, alongside viewing site data, they are
allowed to ``create`` (a site) and ``record`` data.

* ``create`` will require the user to enter the new site's name, location,
  type, and a brief description.

* To ``record`` data, the user will need to select the school (they represent/
  are from), the site they visited, and a data sheet template.


**After Selecting a Site**

The page will display the site's name, type, and description alongside an image
of the location.

Beneath ``Data`` will be a series of checkboxes corresponding to the available
data templates/sheets (e.g. Water Quality, Canopy Cover, etc) for the site.
Once they select which field they'd like to display, users are given the option
to view the site's compiled data in a (raw data) table or as a graph. If they
so choose, they can also ``export`` the selected site data as a CSV.

Once the user has selected the format in which they'd like to view the data, 
they will be redirected to a new page showing either data tables or graphs of
the chosen templates.

Additionally, there will be an option to ``compare`` data between StreamWebs'
sites. Eventually, functionality will be added so that users can compare
StreamWebs site data to other (outside) resources.

So moving on to how ``compare`` function itself works. When the option is
selected, the user will be brought to a new page in which they can choose the
available sites to compare against. Once they hit the ``compare`` button again,
they'll be met with a page displaying multiple graphs of the chosen sites'
data.

**Future**

The current StreamWebs site allows an authenticated user to upload pictures,
excel datasheets, and word documents. This functionality is open to all users.
While not high priority as of now, the ability to upload is something to
consider for later. 

.. note:: 
  
    ``compare`` is allowable for only one data model at a time. In other words,
    a user can't compare a site's Water Quality, Macroinvertabrates, and Canopy
    Cover all at once.

**About Site Stewards and Filtering**

Alongside general site info and data view options, a selected ``Sites`` page
will also contain a list of ``Site Stewards``. These "stewards" are actually
the schools that have participated in gathering that site's data.

Rather than view all compiled data, the user can filter what they see according
to school. So after selecting their desired template(s), the user can click the
``graph``, ``table``, or ``export`` buttons located next to their school name
in the list of ``Site Stewards``.
