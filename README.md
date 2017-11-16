# StreamWebs
[![Build Status](https://travis-ci.org/osuosl/streamwebs.svg?branch=develop)](https://travis-ci.org/osuosl/streamwebs)

This repository will be used to help track issues and share files for the 
existing Streamwebs site during the transition to a possible re-write of the 
application.

To set up a dev instance of StreamWebs, copy ``Dockerfile.env.dist`` to 
``Dockerfile.env``. You will also have to copy ``settings.py.dist`` to
``settings.py`` (located in ``streamwebs_frontend/streamwebs_frontend``). Then,
run the following:
```
$ docker-compose build
$ docker-compose up
```

The following is a list of the more common and more useful docker commands: 
- ``docker-compose build`` will build the necessary containers 
- ``docker-compose build --no-cache --pull`` does a full from-scratch build;
  you can run this when the changes made to the docker environment are not
taking effect 
- ``docker-compose up`` runs the application
- ``docker-compose run web bash`` is like docker-compose up but also provides
  an interactive shell
- ``docker-compose run --service-ports --rm web bash`` exposes the ports
  described for the web service and removes the container upon completion
- `docker-compose kill` stops services that are running
- `docker-compose rm` removes all the containers associated with the
  application's services
- `docker-compose ps` lists all the running containers


**Note that docker-compose and docker commands may need to be run as root with
the ``sudo`` prefix.**

If you run into this error:
```
ERROR: stat /home/thai/projects/streamwebs: too many levels of symbolic links
```
restarting docker should fix the problem. The command to do so is
``sudo systemctl restart docker``


Another note: after running ``docker-compose up``, docker doesn't print the
standard "django app is running" output. Just know that it is.

You can check that this is true by going to ``localhost:8000/streamwebs`` in
your browser.


### Miscellaneous Tips
Run ``flake8 streamwebs_frontend --exclude streamwebs_frontend/streamwebs/migrations``
to exclude the migrations directory when linting.

If you'd like to access the postgresql database, open up an interactive shell
with ``docker-compose run web bash``. Then run the following command:
``psql -h $POSTGRES_HOST -d streamwebs -U $POSTGRES_USER. This will bring you
to the postgres interactive terminal.
