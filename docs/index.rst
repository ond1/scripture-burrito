.. You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Scripture Burrito Specification
================================

:Status: Working Draft
:Date: |today|

.. image:: ../logo/burrito_logo.png

Scripture Burrito is a standard for exchanging Bible translation projects between tools. At the core is a metadata file — the *burrito* — that describes every file in a project: what it contains, what part of Scripture it covers, and what role it plays. The same burrito can be stored as a zip file, a directory, a GitHub repository, a database, or delivered via API.

All burritos share a common structure — see :ref:`burrito-structure`. Flavor-specific fields are documented below.

Scripture Burrito currently defines these flavors:

.. Note: flavor names below are plain text (not :ref: links) to avoid showing
   "Scripture Text Specification" as a redundant link — the Specification link
   already appears in the [Specification | Tutorial | Example] bracket.

- Scripture Text — USFM, USX, or USJ text translations
  [:ref:`Specification <scripture_text_flavor>` | :ref:`Tutorial <tutorial-textTranslation>` | :ref:`Example <examples-textTranslation>`]
- Scripture Audio — recorded audio translations
  [:ref:`Specification <scripture_audio_flavor>` | :ref:`Tutorial <tutorial-audioTranslation>` | :ref:`Example <examples-audioTranslation>`]
- Alignment — word-level or timecode alignment between two texts
  [:ref:`Specification <alignment_flavor>` | :ref:`Tutorial <tutorial-alignment>` | :ref:`Example <examples-alignment>`]
- Wrapper — groups related burritos together, such as a text and audio burrito for the same translation
  [:ref:`Specification <wrapper_flavor>` | :ref:`Tutorial <tutorial-wrapper>` | :ref:`Example <examples-wrapper>`]

Any flavor can also be extended:

- Derived — burritos produced from other burritos, such as back-translations and publication artifacts
  [:ref:`Specification <derived_flavor>` | :ref:`Tutorial <tutorial-derived>` | :ref:`Example <examples-textTranslation_derived>`]
- Custom — defining your own nonstandard flavor using the ``x-`` prefix
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
