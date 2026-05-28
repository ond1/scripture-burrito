.. You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Scripture Burrito Documentation
================================

.. image:: ../logo/burrito_logo.png

Scripture Burrito is a standard for packaging and describing Bible translation projects. If you are building tools that create, exchange, or archive Scripture translations — or if you need to move a translation project between tools — this specification tells you how to package it so that any conforming tool can understand what it contains.

The core of Scripture Burrito is a metadata file that describes all the files in a project: what each file is, what part of Scripture it covers, and what role it plays. That metadata, together with the files it describes, is called a *burrito*. A burrito can be distributed as a zip file, a directory, a GitHub repository, a database, or via API.

Scripture Burrito currently defines two flavors:

- :ref:`scripture_text_flavor` — USFM, USX, or USJ text translations
- :ref:`scripture_audio_flavor` (beta) — recorded audio translations

New flavors can be proposed using the ``x-`` extension mechanism; see :ref:`extending_scripture_burrito`.

Documentation
=============

.. toctree::
   :maxdepth: 4

   introduction/index
   schema_docs/index
   flavors/index
   examples/index
   glossary
