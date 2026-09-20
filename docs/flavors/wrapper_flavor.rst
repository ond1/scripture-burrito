.. _wrapper_flavor:

########################################
Scripture Burrito Wrapper Specification
########################################


Wrapper Flavor
==========================

Overview
------------

A Scripture Burrito Wrapper provides a way to group multiple related
Scripture Burritos into a single project or distribution. Each contained
burrito remains an independent, self-contained Scripture Burrito with its
own metadata and flavor.

A wrapper does not define or alter the flavor of the contained burritos.
Instead, it identifies the burritos that belong together and describes
their relationship to the overall project.

A wrapper can contain different Scripture Burrito flavors, allowing
related resources such as audio translations, text translations, project
management data, intellectual property information, and other supported
flavors to be distributed together.

The wrapper is represented by a `wrapper.json` file located at the root
of the wrapper package.

The following example shows a Scripture Burrito Wrapper containing four related Scripture Burritos. 
The wrapper contains a data burrito providing supplemental project information, a text 
translation burrito containing specific Bible text derived from the source content, an audio 
translation burrito containing information specific to the biblical audio files in the directory 
and representing the primary source content, and an intellectual property burrito containing 
supporting rights and licensing information:

.. admonition:: Full Scripture Burrito Wrapper
   :class: example

   .. code-block:: json

      {
        "meta": {
          "name": {
            "en": "Sample Burrito Burrito Wrapper"
          },
          "version": "0.0.1",
          "generator": {
            "name": "Audio Project Manager Train",
            "version": "4.6.0.alpha.0"
          },
          "dateCreated": "2026-08-13",
          "description": {
            "en": "A new burrito wrapper for Sample Burrito"
          },
          "abbreviation": {
            "en": "SEHSAM"
          },
          "defaultLocale": "en"
        },
        "format": "scripture burrito wrapper",
        "contents": {
          "burritos": [
            {
              "id": "SEHSAM-aPMData",
              "path": "data",
              "role": "supplemental"
            },
            {
              "id": "SEHSAM-text",
              "path": "text",
              "role": "derived"
            },
            {
              "id": "SEHSAM-audio",
              "path": "audio",
              "role": "source"
            },
            {
              "id": "SEHSAM-intellectualProperty",
              "path": "intellectualproperty",
              "role": "supplemental"
            }
          ]
        }
      }

This wrapper contains four Scripture Burritos, each located in a separate
directory within the wrapper package. The directory structure is as
follows::

    project/
    ├── wrapper.json
    ├── audio/
    │   └── metadata.json
    ├── text/
    │   └── metadata.json
    ├── apmdata/
    │   └── metadata.json
    └── intellectualproperty/
        └── metadata.json

Wrapper Structure
-----------------

A wrapper MUST contain the following top-level properties:

* `meta`
* `format`
* `contents`

In the following sections we will break down and describe each property and its sub-properties they contain.

Meta
------------

The meta property contains metadata describing the Scripture Burrito Wrapper itself. It identifies and provides information 
about the wrapper as a whole and optional descriptive information. 
The metadata does not apply to the individual Scripture Burritos contained within the wrapper.

The ``meta`` object describes the wrapper and MUST contain:

* ``name``
* ``version``
* ``generator``
* ``dateCreated``

It MAY also contain:

* ``description``
* ``abbreviation``
* ``defaultLocale``

The metadata applies to the *wrapper*, rather than to the individual
burritos contained within it. Each contained burrito MUST provide its own
``metadata.json``.

Name
~~~~~~~~~~~~~~~~~~~~~~~~

The ``name`` property contains one or more localized names for the
wrapper.

The property is an object in which each property name is a language or
locale code, and the corresponding property value is the human-readable
name of the wrapper in that language or locale.

For example::

    "name": {
      "en": "Sample Burrito Burrito Wrapper"
    }

A wrapper MAY provide names in multiple languages or locales::

    "name": {
      "en": "Sample Scripture Project",
      "fr": "Projet biblique exemple"
    }

The language or locale codes SHOULD follow the conventions defined by
the Scripture Burrito specification.

Version
~~~~~~~~~~~~~~~~~~~~~~~~

The ``version`` property identifies the version of the wrapper.

The value MUST be a string. The version applies to the wrapper itself and
does not determine the version of any contained Scripture Burritos.

For example::

    "version": "0.0.1"

Generator
~~~~~~~~~~~~~

The ``generator`` property identifies the software or process that
created the wrapper.

The ``generator`` object MUST contain:

* ``name``
* ``version``

For example::

    "generator": {
      "name": "Audio Project Manager Train",
      "version": "4.6.0.alpha.0"
    }

The ``name`` property is specified by the creator. This property best describes the name of the software.
The ``version`` property specifies the version of the software used to create the wrapper and is presented as a textual data.

Date Created
~~~~~~~~~~~~~~~~

The ``dateCreated`` property identifies the date on which the wrapper
was created.

The value MUST be represented as a date in the format ``YYYY-MM-DD``. This is in the
**ISO 8601 calendar date format**.

Where:

* ``YYYY`` = four-digit year → ``2026``
* ``MM`` = two-digit month → ``08`` (August)
* ``DD`` = two-digit day → ``13``

For example::

    "dateCreated": "2026-08-13"

The ``dateCreated`` property applies to the wrapper itself and does not
necessarily represent the creation date of the contained burritos.

Description
~~~~~~~~~~~~~~~~~~

The optional ``description`` property provides descriptive text
about the wrapper.

The description MAY be provided in multiple languages or locales.

For example::

    "description": {
      "en": "A new burrito wrapper for Sample Burrito"
    }

Abbreviation
~~~~~~~~~~~~~~~~~~~~~~~~

The optional ``abbreviation`` property provides a short name or
abbreviation for the wrapper.

The abbreviation MAY be provided in multiple languages or locales.

.. admonition:: Abbreviation Example
   :class: example

   .. code-block:: json

      "abbreviation": {
        "en": "SEHSAM"
      }

Default Locale
~~~~~~~~~~~~~~~~~~

The ``defaultLocale`` property identifies the default language or locale
of the wrapper.

The value MUST be a valid BCP 47 language tag.

For example::

    "defaultLocale": "en"

The value ``en`` identifies the English language. More specific language
tags MAY be used where required, such as ``en-US`` for English as used
in the United States or ``en-GB`` for English as used in the United
Kingdom.


Contents
------------

The `contents` object MUST contain a `burritos` array.

Each entry identifies one Scripture Burrito contained within the wrapper.


.. admonition:: Contents Example
   :class: example

   .. code-block:: json

      "contents": {
        "burritos": [
          {
            "id": "ENGSEB2-audio",
            "path": "audio",
            "role": "source"
          },
          {
            "id": "ENGSEB2-text",
            "path": "text",
            "role": "derived"
          }
        ]
      }


The `burritos` array MUST contain at least one entry. Each entry MUST
contain:

* `id`
* `path`
* `role`

The `path` is relative to the directory containing `wrapper.json`.

Contained Burritos
-----------------------

Each entry in ``contents.burritos`` MUST identify a valid Scripture
Burrito or another valid Scripture Burrito Wrapper.

The ``path`` is relative to the directory containing ``wrapper.json`` and
MUST identify the directory containing the burrito's ``metadata.json`` or,
in the case of a nested wrapper, its ``wrapper.json``.

Nested wrappers are permitted, but circular references MUST NOT occur.

The flavor of a contained burrito is determined by its own
``metadata.json``. The wrapper MUST NOT duplicate or override the flavor
information.


Burrito Roles
------------------

The ``role`` property describes the relationship of a contained burrito
to the other burritos in the wrapper.

The standard roles are:

+-------------------+-----------------------------------------------------------+
| Role              | Description                                               |
+===================+===========================================================+
| ``source``        | Primary or source content.                                |
+-------------------+-----------------------------------------------------------+
| ``derived``       | Content produced from another burrito.                    |
+-------------------+-----------------------------------------------------------+
| ``supplemental``  | Supporting material that is not itself the primary        |
|                   | Scripture deliverable.                                    |
+-------------------+-----------------------------------------------------------+

Custom roles MAY be used where supported by the Scripture Burrito
specification. Custom roles SHOULD begin with ``x-``.

The role is a property of the relationship within the wrapper and does
not determine the flavor of the contained burrito.


Supporting Multiple flavors
---------------------------------

A wrapper MAY contain any combination of supported Scripture Burrito
flavors.

For example, an audio Scripture project could contain:

* `audioTranslation`
* `textTranslation`
* `intellectualProperty`
* `apmData`

The wrapper therefore provides a mechanism for grouping related
Scripture Burritos without requiring the individual flavors to be
merged into a single burrito.

The flavor of each contained burrito is determined by its own
`metadata.json`.

.. admonition:: Multiple Flavors
   :class: example

   .. code-block:: json
      {
        "id": "SEHSAM-audio",
        "path": "audio",
        "role": "source"
      }


The flavor of this burrito is determined by:

audio/metadata.json



.. admonition:: Contained Burrito Example
   :class: example

   .. code-block:: json

      {
        "id": "SEHSAM-text",
        "path": "text",
        "role": "derived"
      }

gets its flavor from:

text/metadata.json


This separation allows each flavor to evolve independently while still
allowing related resources to be distributed together.

Wrapper and Contained Burrito Independence
------------------------------------------------

The wrapper and the contained Scripture Burritos have separate scopes.

The wrapper describes the collection of resources and the relationships
between them. It MUST NOT modify, override, or replace the metadata of a
contained burrito.

Each contained Scripture Burrito remains independently defined and
validated according to its own flavor specification.

For example, information describing an audio translation belongs in the
metadata of the audio Scripture Burrito, rather than being duplicated in
the wrapper.

The wrapper SHOULD contain only information that applies to the
collection as a whole or describes the relationship between the
contained resources.


Wrapper flavor 
---------------------

A wrapper MUST NOT make assumptions about the flavor of a contained
burrito. The flavor MUST be determined from the metadata of the
contained burrito.

A wrapper MAY contain multiple burritos of the same flavor or burritos
of different flavors.

This allows the wrapper to group related resources while keeping each
Scripture Burrito flavor independently defined and validated.


Nested Wrappers
---------------------

A Scripture Burrito Wrapper MAY contain another Scripture Burrito
Wrapper.

A nested wrapper MUST itself be a valid Scripture Burrito Wrapper and
MUST contain its own ``wrapper.json``.

For example::

    project/
    ├── wrapper.json
    ├── translations/
    │   ├── wrapper.json
    │   ├── audio/
    │   │   └── metadata.json
    │   └── text/
    │       └── metadata.json
    └── supporting/
        └── wrapper.json

The ``path`` of a nested wrapper MUST identify the directory containing
the nested ``wrapper.json``.

A wrapper MUST NOT directly or indirectly contain itself. Circular
references between wrappers are not permitted.


Validation
------------------

A Scripture Burrito Wrapper MUST be independently valid according to
this specification.

Validation of a wrapper MUST verify that:

* ``wrapper.json`` exists at the root of the wrapper package.
* The ``format`` property has the value ``scripture burrito wrapper``.
* The required ``meta`` properties are present.
* The ``contents`` object contains a ``burritos`` array.
* The ``burritos`` array contains at least one entry.
* Each burrito entry contains ``id``, ``path``, and ``role``.
* Each ``path`` identifies a valid Scripture Burrito or Scripture Burrito
  Wrapper within the wrapper package.
* A contained Scripture Burrito contains its required ``metadata.json``.
* A contained Scripture Burrito Wrapper contains its required
  ``wrapper.json``.
* No circular references exist between nested wrappers.

Validation of each contained Scripture Burrito MUST be performed
according to the specification for that burrito's flavor.

The wrapper therefore provides a mechanism for validating the
relationship and structure of the collection, while the individual
burrito specifications remain responsible for validating the contents of
each burrito.


Additional Examples
-------------------------

Additional examples and sample Scripture Burrito audio translation
packages can be found in the ``sb_audioTranslation`` GitHub repository::

    https://github.com/bible-technology/sb_audioTranslation
