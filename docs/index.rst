.. You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Scripture Burrito Documentation
================================

.. image:: ../logo/burrito_logo.png

Scripture Burrito is a standard for packaging and describing Bible translation projects. If you are building tools that create, exchange, or archive Scripture translations — or if you need to move a translation project between tools — this specification tells you how to package it so that any conforming tool can understand what it contains.

The core of Scripture Burrito is a metadata file that describes all the files in a project: what each file is, what part of Scripture it covers, and what role it plays. That metadata, together with the files it describes, is called a *burrito*. A burrito is not bound to a physical format, for instance, the same burrito can be distributed as a zip file, a directory, a GitHub repository, a database, or via API.

All burritos share a common structure — see :ref:`burrito-structure`. Flavor-specific fields are documented below.

Scripture Burrito currently defines these flavors:

- :ref:`scripture_text_flavor` — USFM, USX, or USJ text translations
  [:ref:`Specification <scripture_text_flavor>` | :ref:`Tutorial <tutorial-textTranslation>` | :ref:`Example <examples-textTranslation>`]
- :ref:`scripture_audio_flavor` — recorded audio translations
  [:ref:`Specification <scripture_audio_flavor>` | :ref:`Tutorial <tutorial-audioTranslation>` | :ref:`Example <examples-audioTranslation>`]
- :ref:`alignment_flavor` — word-level or timecode alignment between two texts
  [:ref:`Specification <alignment_flavor>` | :ref:`Tutorial <tutorial-alignment>` | :ref:`Example <examples-alignment>`]
- :ref:`wrapper_flavor` — groups related burritos together, such as a text and audio burrito for the same translation
  [:ref:`Specification <wrapper_flavor>` | :ref:`Tutorial <tutorial-wrapper>` | :ref:`Example <examples-wrapper>`]
- :ref:`derived_flavor` — burritos produced from other burritos, such as back-translations and publication artifacts
  [:ref:`Specification <derived_flavor>` | :ref:`Tutorial <tutorial-derived>` | :ref:`Example <examples-textTranslation_derived>`]
- :ref:`custom_flavors` — defining your own nonstandard flavor using the ``x-`` prefix
  [:ref:`Specification <custom_flavors>`]

Documentation
=============

.. toctree::
   :maxdepth: 1

   introduction/index
   introduction/structure
   tutorials/index
   schema_docs/index
   flavors/index
   examples/index
   glossary
