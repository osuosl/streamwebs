# StreamWebs
[![Build Status](https://travis-ci.org/osuosl/streamwebs.svg?branch=develop)](https://travis-ci.org/osuosl/streamwebs)

This repository will be used to help track issues and share files for the existing Streamwebs site during the
transition to a possible re-write of the application.

To set up a dev instance of StreamWebs, copy ``Dockerfile.env.dist`` to ``Dockerfile.env``. You will also have to copy
``settings.py.dist`` to ``settings.py`` (located in ``streamwebs_frontend/streamwebs_frontend``). Then, run the
following:

``` console
$ docker-compose build
$ docker-compose up
```

The following is a list of the more common and more useful docker commands:

- ``docker-compose build`` will build the necessary containers
- ``docker-compose build --no-cache --pull`` does a full from-scratch build; you can run this when the changes made to
  the docker environment are not taking effect.
- ``docker-compose up`` runs the application
- ``docker-compose run web bash`` is like docker-compose up but also provides an interactive shell
- ``docker-compose run --service-ports --rm web bash`` exposes the ports described for the web service and removes the
  container upon completion
- `docker-compose kill` stops services that are running
- `docker-compose rm` removes all the containers associated with the application's services
- `docker-compose ps` lists all the running containers

After running ``docker-compose up``, docker doesn't print the standard "django app is running" output. Instead, just go
to http://localhost:8000 instead.

### Miscellaneous Tips

Run ``flake8 streamwebs_frontend --exclude streamwebs_frontend/streamwebs/migrations`` to exclude the migrations
directory when linting.

If you'd like to access the postgresql database, open up an interactive shell with ``docker-compose run web bash``.
Then run the following command: ``PGPASSWORD=$POSTGRES_PASSWORD psql -h postgres_host -U $POSTGRES_USER streamwebs``.
This will bring you to the postgres interactive terminal. You can also do get access running ``python
streamwebs_frontend/manage.py dbshell``.

If you would like to drop the ``streamwebs`` database each time the web container runs, add ``STREAMWEBS_DROP=1`` to
your ``Dockerfile.env`` file.

If you would like to only run tests, add ``STREAMWEBS_TEST=1`` to your ``Dockerfile.env`` file. Keep in mind this
doesn't run the django web server and only runs the tests.

If you want to automatically import the CSV data, you need to add both `STREAMWEBS_DROP=1`` and
``STREAMWEBS_IMPORT_DATA=1`` to your ``Dockerfile.env`` file.
