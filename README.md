# StreamWebs

This repository will be used to help track issues and share files for the 
existing Streamwebs site during the transition to a possible re-write of the 
application.

To set up a dev instance of StreamWebs, copy ``Dockerfile.env.dist`` to 
``Dockerfile.env``. Then, run the following:
```
$ sudo docker-compose build
$ sudo docker-compose run web
```

Note that after running ``sudo docker-compose run web``, docker doesn't print
the standard "django app is running" output. Just know that it is.

You can check that this is true by going to ``localhost:8000/streamwebs`` in
your browser.
