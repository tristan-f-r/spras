Container Frameworks
====================

SPRAS supports several container frameworks, which can be configured in the ``container_framework`` setting in your config:

* ``docker``: (default) uses Docker, the most widely used tool (at the time of writing) for running images
* ``singularity``: uses Apptainer (previously known as singularity), useful for interfacing with high performance computing software - this is used for SPRAS's HTCondor integration.
* ``dsub``: uses dsub, a tool for running batch images in the cloud.

Some container frameworks may take in extra options in their configuration or via environment variables:

.. TODO: in-rtd singularity documentation

dsub
----

``dsub`` can be configured with the ``dsub`` property in your config. The only option available is ``local``,
which decides whether ``dsub`` uses your Docker installation locally, or if it uses google cloud. By default, ``local`` is false.

``dsub`` also requires some initial setup. The ``gcloud`` command-line interface must be installed on your computer (see `installation instructions <https://cloud.google.com/sdk/docs/install>`_),
and you must specify two environment variables:

* ``GOOGLE_PROJECT`` (not required when ``local`` is true): the ID of your project
* ``WORKSPACE_BUCKET``
