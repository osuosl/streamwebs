.. _dev_sites:

=====
Sites
=====

Sites consist of a name, description, and location. A photo of the physical
location is optional, a default image will be provided if no new images is
uploaded.

In the previous application, Sites were called Projects, but the functionality
is essentially the same.

Data is directly associated with a site, all datasheets must have a one-to-one
associate with a Site.

The Site Model
--------------

We use Model Managers on most streamwebs models. See `Django Model Managers`_
documentation for information on why and how to use managers.

**The Site model manager**

.. literalinclude:: ../../../streamwebs_frontend/streamwebs/models.py
   :pyobject: SiteManager

**The Site model**

.. literalinclude:: ../../../streamwebs_frontend/streamwebs/models.py
   :pyobject: Site


The Site Form
-------------

Sites can be added or edited using the Site form.

**The Site form**

.. literalinclude:: ../../../streamwebs_frontend/streamwebs/forms.py
   :pyobject: SiteForm


The Site Views
--------------

There are several views relating to Sites. There are the standard views for
View, List, Create, Update, and Deactivate. Site views always include a map
object displaying the Site location.

sites
~~~~~

In the sites view (list all sites), all available sites are presented as
markers on Google map of Oregon. This view also allows searching by name,
selecting a site from a pull-down list, and creating a new site. Any registered
user may create a new site.

site
~~~~

In the site view (view an individual site), the site location is displayed on a
map along with the photo of the site and all data associated with the site.
Data is displayed as a table of datasheets organized by the school which
submitted the data.

Additionally, if graphable data is associated with the site (Water Quality,
Macroinvertabrates, or Riparian Transect), buttons will appear to view graphs
of the sumbitted data.

Finally, links are provided to add data or export data to a CSV file.

update_site
~~~~~~~~~~~

This view renders the Site form and allows the user to change the name,
location, image or description.

deactivate_site
~~~~~~~~~~~~~~~

The deactivate site view will 'delete' the site by setting its ``active`` field
to False. This can only be done if no data is associated with this site.


**Site Views**

.. literalinclude:: ../../../streamwebs_frontend/streamwebs/views/general.py
   :language: python
   :lines: 42-190


.. _`Django Model Managers`: https://docs.djangoproject.com/en/1.11/topics/db/managers/
