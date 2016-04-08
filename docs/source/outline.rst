.. _project_outline:

===============
Project Outline
===============

Current plan for the StreamWebs rewrite. For a visual representation, 
refer to `this`_.

On the site's homepage, the user will be able to navigate to one of the
following pages:

* Login
* Analyze/Learn
* Resources

.. _this: http://i.imgur.com/XqOmLQn.jpg


Login
-----

After login, the user will be taken to a central ``Sites`` page.

.. note::

    Alongside **Users**, basic CRUD will need to be implemented for
    **Resources** and **Map/Sites** as well.

Analyze/Learn
-------------

The ``Analyze/Learn`` page will also redirect the user to ``Sites``.

Resources
---------

Resources will contain all of StreamWebs' data sheets along with
external/internal links to supplementary information.

Sites
-----

**Default**

Specific sites should be searchable by name. Alongside that, there should also
be a map display with markers denoting site locations. Users should be able to
navigate to a specific site's page by clicking on its marker on the map.

**After Selecting a Site**

If the user has been authenticated, alongside viewing site data, they are
allowed to ``create`` (a site) and ``record`` data. If not, they will only
be able to view current site data.

.. note::

    Currently, the ``create`` option will only ask for the new site's location
    and type. Before they can start to ``record``, the user will need to select
    the site as well as a data sheet template.

After selecting a specific site, the page will display its site name, an image
of its location, and a list of different data models (e.g. Water Quality,
Canopy Cover, etc).

If they so choose, a user can ``export`` the selected site data as a CSV.

The ``view`` option will allow them to select between a display of raw or
graphed data. Choosing to view graphed data will redirect the user to a new
page showing the graphed data of the models selected.

Additionally, there will be an option to ``compare`` site data between
StreamWebs and other resources. Doing so will bring the user to a new page in
which they can select where this outside data will come from. Once they hit
compare again, they'll be met with a page displaying multiple graphs of the
site's data.

.. note:: 
  
    ``compare`` is allowable for only one data model at a time. In other words,
    a user can't compare a site's Water Quality, Riparian, and Canopy Cover all
    at once.
