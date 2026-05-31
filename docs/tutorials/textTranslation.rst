.. _tutorial-textTranslation:

#######################
Scripture Text Tutorial
#######################

[:ref:`Specification <scripture_text_flavor>`]  [:ref:`Example <examples-textTranslation>`]

This tutorial walks through creating a Scripture Burrito metadata file for a
Scripture text translation. By the end you will have a valid ``metadata.json``
that can be read by any conforming tool.

**Scenario:** A translation team has finished a New Testament in Zarma (a
language of the Sahel region). The files live in a directory called
``zarma-nt/``. We want to package them as a Scripture Burrito so they can be
exchanged with other tools.

The directory currently looks like this::

   zarma-nt/
       ingredients/
           40MATZARMA.SFM
           41MRKZARMA.SFM
           43JHNZARMA.SFM
           44ACTZARMA.SFM
           dje.ldml
           versification.json

We will build the ``metadata.json`` file section by section.

=============
Common Fields
=============

*These fields are common to all burritos — see* :ref:`burrito-structure` *for the full specification.*

---------
1. Format
---------

Every burrito begins with the ``format`` field. This identifies the file as a
Scripture Burrito rather than anything else::

   {
     "format": "scripture burrito",

That single field is what every conforming tool checks first.

---------------
2. Meta section
---------------

The ``meta`` section records who generated this file and when::

     "meta": {
       "version": "1.0.0",
       "category": "source",
       "generator": {
         "softwareName": "MyTranslationTool",
         "softwareVersion": "2.3.1",
         "userName": "Fatima Maïga"
       },
       "defaultLocale": "dje",
       "dateCreated": "2025-11-04T09:00:00+01:00",
       "normalization": "NFC"
     },

* ``version`` — the Scripture Burrito schema version this file conforms to.
* ``category`` — ``"source"`` means this is an editable project, not a
  publication artifact. Use ``"distribution"`` for read-only releases.
* ``defaultLocale`` — the BCP-47 tag for the primary language of the project.
  Values in ``localizedNames`` and ``identification.name`` will use this locale
  unless another is specified.
* ``normalization`` — the Unicode normalization form of the text files.

--------------------------
3. Identification section
--------------------------

The ``identification`` section names the project in a human-readable way, and
optionally links it to identifiers in external systems::

     "identification": {
       "name": {
         "en": "Zarma New Testament",
         "dje": "Zarma Neeriya Koyra"
       },
       "description": {
         "en": "New Testament translation into Zarma (Songhay family)"
       },
       "abbreviation": {
         "en": "ZJNT"
       }
     },

* ``name``, ``description``, and ``abbreviation`` are all
  language-tag-to-string maps so the project can be named in multiple languages.

If your project is registered in an external system (such as the Digital Bible
Library), add an ``idAuthorities`` section and reference it from
``identification.primary``::

     "idAuthorities": {
       "dbl": {
         "id": "https://thedigitalbiblelibrary.org",
         "name": {"en": "The Digital Bible Library"}
       }
     },
     "identification": {
       "primary": {
         "dbl": {
           "a3f9c12e887b4d01": {
             "revision": "1",
             "timestamp": "2025-11-04T09:00:00+01:00"
           }
         }
       },
       "name": { "en": "Zarma New Testament" },
       ...
     },

For a new project with no external registry entry, you can omit
``idAuthorities`` and ``identification.primary`` entirely.

--------------------
4. Languages section
--------------------

The ``languages`` array lists every language present in the translation::

     "languages": [
       {
         "tag": "dje",
         "name": {
           "en": "Zarma",
           "dje": "Zarmaciine"
         }
       }
     ],

* ``tag`` must be a valid BCP-47 language tag. For minority languages, check
  `ISO 639-3 <https://iso639-3.sil.org/>`_ for the three-letter code.
* ``name`` follows the same locale-map pattern as ``identification.name``.

-------------------
5. Agencies section
-------------------

The ``agencies`` array records which organisations are responsible for this
content::

     "agencies": [
       {
         "id": "https://seedcompany.com",
         "roles": ["rightsHolder", "content"],
         "url": "https://seedcompany.com",
         "name": {
           "en": "Seed Company"
         },
         "abbr": {
           "en": "SC"
         }
       }
     ],

* ``roles`` is a list drawn from: ``"rightsHolder"``, ``"content"``,
  ``"publication"``, ``"management"``, ``"finance"``, ``"qa"``.
* ``id`` is a URI that uniquely identifies the agency. If the agency is
  registered in an authority referenced in ``idAuthorities``, use that
  authority's scoped format (e.g. ``"dbl::54650cfa5117ad690fb05fb6"``);
  otherwise a stable URL for the organisation is fine.

---------------------
6. Common Ingredients
---------------------

The ``ingredients`` object maps every file path (relative to the burrito root)
to a descriptor. These fields appear in every burrito regardless of flavor:

* **file path** (the key) — relative to the burrito root, using forward
  slashes. Must match the actual layout exactly.
* **checksum** — used by receiving tools to verify file integrity. MD5 is
  currently the standard algorithm.
* **mimeType** — identifies the file format. Allowed values are
  flavor-specific; see below.
* **size** — file size in bytes.
* **scope** — for text files, lists the books the file contains. Each book
  code maps to either an empty array (whole book) or a list of chapter numbers.
* **role** — for support files that are not primary text. Allowed values are
  flavor-specific; see below.

=====================
Scripture Text Fields
=====================

*These fields are specific to the Scripture Text flavor — see*
:ref:`scripture_text_flavor` *for the full specification.*

---------------
7. Type section
---------------

The ``type`` section declares the flavor — the kind of content this burrito
contains. For a text translation::

     "type": {
       "flavorType": {
         "name": "scripture",
         "flavor": {
           "name": "textTranslation",
           "usfmVersion": "3.1",
           "translationType": "firstTranslation",
           "audience": "common",
           "projectType": "standard"
         },
         "currentScope": {
           "MAT": [],
           "MRK": [],
           "JHN": [],
           "ACT": []
         }
       }
     },

* ``flavorType.name`` is always ``"scripture"`` for biblical text.
* ``flavor.name`` is ``"textTranslation"`` for USFM/USX/USJ text.
* ``currentScope`` lists every book present, using three-letter USFM book codes.
  An empty array (``[]``) means all chapters of that book are included; you can
  restrict to specific chapters with a list of integers.
* ``translationType`` — use ``"firstTranslation"`` for a language that has
  never had this testament before, or ``"revision"`` if this updates an
  existing translation.
* ``audience`` — ``"common"`` covers general readership. See
  :ref:`scripture_text_flavor` for the full set of values.
* ``projectType`` — ``"standard"`` for a normal translation.

------------------------------
8. Flavor-Specific Ingredients
------------------------------

Text ingredients must use one of these MIME types:

* ``"text/x-usfm"`` for USFM files (``.SFM``, ``.USFM``)
* ``"application/xml"`` for USX files
* ``"application/json"`` for USJ files (also set ``"role": "text"``)

Support file roles defined for this flavor:

* ``"versification"`` — a ``versification.json`` defining the verse structure.
  Should be present; must use ``"mimeType": "application/json"``.
* ``"localedata"`` — an ``.ldml`` locale file. Should be present; must use
  ``"mimeType": "application/xml"``.

Every book declared in ``type.flavorType.currentScope`` must have at least one
text ingredient whose ``scope`` covers that book.

The full ``ingredients`` object for the Zarma New Testament::

     "ingredients": {
       "ingredients/40MATZARMA.SFM": {
         "checksum": {"md5": "a1b2c3d4e5f6..."},
         "mimeType": "text/x-usfm",
         "size": 154322,
         "scope": {"MAT": []}
       },
       "ingredients/41MRKZARMA.SFM": {
         "checksum": {"md5": "f6e5d4c3b2a1..."},
         "mimeType": "text/x-usfm",
         "size": 98500,
         "scope": {"MRK": []}
       },
       "ingredients/43JHNZARMA.SFM": {
         "checksum": {"md5": "1a2b3c4d5e6f..."},
         "mimeType": "text/x-usfm",
         "size": 141200,
         "scope": {"JHN": []}
       },
       "ingredients/44ACTZARMA.SFM": {
         "checksum": {"md5": "6f5e4d3c2b1a..."},
         "mimeType": "text/x-usfm",
         "size": 210450,
         "scope": {"ACT": []}
       },
       "ingredients/dje.ldml": {
         "checksum": {"md5": "deadbeef1234..."},
         "mimeType": "application/xml",
         "size": 2840,
         "role": "localedata"
       },
       "ingredients/versification.json": {
         "checksum": {"md5": "feedcafe5678..."},
         "mimeType": "application/json",
         "size": 4300,
         "role": "versification"
       }
     }

=================
The complete file
=================

Putting it all together::

   {
     "format": "scripture burrito",
     "meta": {
       "version": "1.0.0",
       "category": "source",
       "generator": {
         "softwareName": "MyTranslationTool",
         "softwareVersion": "2.3.1",
         "userName": "Fatima Maïga"
       },
       "defaultLocale": "dje",
       "dateCreated": "2025-11-04T09:00:00+01:00",
       "normalization": "NFC"
     },
     "identification": {
       "name": {
         "en": "Zarma New Testament",
         "dje": "Zarma Neeriya Koyra"
       },
       "description": {
         "en": "New Testament translation into Zarma (Songhay family)"
       },
       "abbreviation": {
         "en": "ZJNT"
       }
     },
     "languages": [
       {
         "tag": "dje",
         "name": {
           "en": "Zarma",
           "dje": "Zarmaciine"
         }
       }
     ],
     "type": {
       "flavorType": {
         "name": "scripture",
         "flavor": {
           "name": "textTranslation",
           "usfmVersion": "3.1",
           "translationType": "firstTranslation",
           "audience": "common",
           "projectType": "standard"
         },
         "currentScope": {
           "MAT": [],
           "MRK": [],
           "JHN": [],
           "ACT": []
         }
       }
     },
     "agencies": [
       {
         "id": "https://seedcompany.com",
         "roles": ["rightsHolder", "content"],
         "url": "https://seedcompany.com",
         "name": {"en": "Seed Company"},
         "abbr": {"en": "SC"}
       }
     ],
     "ingredients": {
       "ingredients/40MATZARMA.SFM": {
         "checksum": {"md5": "a1b2c3d4e5f6..."},
         "mimeType": "text/x-usfm",
         "size": 154322,
         "scope": {"MAT": []}
       },
       "ingredients/41MRKZARMA.SFM": {
         "checksum": {"md5": "f6e5d4c3b2a1..."},
         "mimeType": "text/x-usfm",
         "size": 98500,
         "scope": {"MRK": []}
       },
       "ingredients/43JHNZARMA.SFM": {
         "checksum": {"md5": "1a2b3c4d5e6f..."},
         "mimeType": "text/x-usfm",
         "size": 141200,
         "scope": {"JHN": []}
       },
       "ingredients/44ACTZARMA.SFM": {
         "checksum": {"md5": "6f5e4d3c2b1a..."},
         "mimeType": "text/x-usfm",
         "size": 210450,
         "scope": {"ACT": []}
       },
       "ingredients/dje.ldml": {
         "checksum": {"md5": "deadbeef1234..."},
         "mimeType": "application/xml",
         "size": 2840,
         "role": "localedata"
       },
       "ingredients/versification.json": {
         "checksum": {"md5": "feedcafe5678..."},
         "mimeType": "application/json",
         "size": 4300,
         "role": "versification"
       }
     }
   }

==========
Next steps
==========

* Add ``localizedNames`` to provide translated book names for display in tools
  — see the full :ref:`examples-textTranslation` for the pattern.
* Add a ``copyright`` section if this project will be shared publicly.
* If you are deriving a daughter project from this translation (e.g. a
  back-translation or a study Bible), see :ref:`examples-textTranslation_derived`.
* For the complete field reference see :ref:`scripture_text_flavor`.
