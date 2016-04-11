.. _project_outline:

===============
Project Outline
===============

Current plan for the StreamWebs rewrite. For a visual representation, 
refer to `this`_.

For now, the site's homepage will act as a static intro page that contains a
brief description about what StreamWebs is. Make sure the page is editable for
later renditions of the site.

On ``Home``, the user will be able to navigate to one of the
following pages:

* Login
* Sites
* Resources

.. _this: http://i.imgur.com/XqOmLQn.jpg


Login
-----

After login, the user will be taken to the central ``Sites`` page.

.. note::

    Alongside **Users**, basic CRUD will need to be implemented for
    **Resources** and **Map/Sites** as well.

Resources
---------

Resources will contain all of StreamWebs' data sheets along with
external/internal links to supplementary information and the curriculum. Make
sure this page is editable through the admin panel as well.

Sites
-----

**Default Display**

Specific sites should be searchable by name. Alongside that, there should also
be a map display with markers denoting site locations. Users should be able to
navigate to a specific site's page by clicking on its marker on the map. 
Underneath the map, there should be pull down menu listing all the site names.

.. note::

    Map pin size for each site will vary depending on the number of data sheets
    inputted for that location.

**If Authenticated**

If the user has been authenticated, alongside viewing site data, they are
allowed to ``create`` (a site) and ``record`` data. If not, they will only
be able to view current site data.

* ``create`` will require the user to enter the new site's location, type, and
  a brief description.

* To ``record`` data, the user will need to select the school (they represent/
  are from), the site they visited, and a data sheet template.


**After Selecting a Site**

The page will display the site's name, type, and description alongside an image
of its location.

Beneath ``Data`` will be a series of checkboxes corresponding to the available
data templates/sheets (e.g. Water Quality, Canopy Cover, etc) for the site.
Once they select which field they'd like to display, users are given the option
to view the site's compiled data in a (raw data) table or as a graph. If they
so choose, they can also ``export`` the selected site data as a CSV.

Once the user has selected the format in which they'd like to view the data, 
they will be redirected to a new page showing either data tables or graphs of
the chosen templates.

Additionally, there will be an option to ``compare`` site data between
StreamWebs and other resources. Doing so will bring the user to a new page in
which they can select where this outside data will come from. Once they hit
compare again, they'll be met with a page displaying multiple graphs of the
site's data.

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
