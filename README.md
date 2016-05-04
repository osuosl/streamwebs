# StreamWebs

This repository will be used to help track issues and share files for the 
existing Streamwebs site during the transition to a possible re-write of the 
application.

To set up a dev instance of StreamWebs, copy ``Dockerfile.env.dist`` to 
``Dockerfile.env``. Then, run the following:
```
$ docker-compose build
$ docker-compose up
```

``docker-compose build`` will build the necessary containers while
``docker-compose up`` runs the application.

**Note that docker-compose and docker commands may need to be run as root with
the ``sudo`` prefix.**

If you run into this error:
```
ERROR: stat /home/thai/projects/streamwebs: too many levels of symbolic links
```
restarting docker should fix the problem. The command to do so is
``sudo systemctl restart docker``

Note that after running ``docker-compose up``, docker doesn't print the
standard "django app is running" output. Just know that it is.

You can check that this is true by going to ``localhost:8000/streamwebs`` in
your browser.
